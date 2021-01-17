# -*- coding: utf-8 -*-
# (c) 2015-2021 Andreas Motl <andreas@getkotori.org>
import time
import json

import arrow
from bunch import Bunch
from cornice.util import to_list
from twisted.logger import Logger, LogLevel
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from twisted.application.service import MultiService, Service
from twisted.python.failure import Failure
from twisted.python.threadpool import ThreadPool

from kotori.daq.decoder import DecoderManager
from kotori.daq.decoder.schema import MessageType, TopicMatchers
from kotori.daq.services import MultiServiceMixin
from kotori.daq.intercom.mqtt import MqttAdapter
from kotori.daq.storage.influx import InfluxDBAdapter
from kotori.util.configuration import read_list
from kotori.util.thimble import Thimble

log = Logger()


class MqttInfluxGrafanaService(MultiService, MultiServiceMixin):

    def __init__(self, channel=None, graphing=None, strategy=None):

        MultiService.__init__(self)

        # TODO: Sanity checks/assertions against channel, graphing and strategy

        # TODO: Make subsystems dynamic
        self.subsystems = ['channel', 'graphing', 'strategy']
        self.channel = channel or Bunch(realm=None, subscriptions=[])
        self.graphing = to_list(graphing)
        self.strategy = strategy

        self.name = u'service-mig-' + self.channel.get('realm', str(id(self)))

    def setupService(self):

        self.log(log.info, u'Bootstrapping')
        self.settings = self.parent.settings

        # Optionally register subsystem component as child service
        for subsystem in self.subsystems:
            if hasattr(self, subsystem):
                subsystem_service = getattr(self, subsystem)
                if isinstance(subsystem_service, Service):
                    log.info('Registering subsystem component "{subsystem}" as service', subsystem=subsystem)
                    self.registerService(subsystem_service)

        # Configure metrics to be collected each X seconds
        metrics_interval = int(self.channel.get('metrics_logger_interval', 60))
        self.metrics = Bunch(tx_count=0, starttime=time.time(), interval=metrics_interval)

        subscriptions = read_list(self.channel.mqtt_topics)
        self.mqtt_service = MqttAdapter(
            name          = u'mqtt-' + self.channel.realm,
            broker_host   = self.settings.mqtt.host,
            broker_port   = int(self.settings.mqtt.port),
            broker_username = self.settings.mqtt.username,
            broker_password = self.settings.mqtt.password,
            callback      = self.mqtt_receive,
            subscriptions = subscriptions)

        self.registerService(self.mqtt_service)

        self.influx = InfluxDBAdapter(settings = self.settings.influxdb)

        # Perform MQTT message processing using a different thread pool
        self.threadpool = ThreadPool()
        self.thimble = Thimble(reactor, self.threadpool, self, ["process_message"])

    def startService(self):
        self.setupService()
        #self.log(log.info, u'Starting')
        MultiService.startService(self)
        self.metrics_twingo = LoopingCall(self.process_metrics)
        self.metrics_twingo.start(self.metrics.interval, now=True)

    def log(self, level, prefix):
        level(u'{prefix} {class_name}. name={name}, channel={channel}',
            prefix=prefix, class_name=self.__class__.__name__, name=self.name, channel=dict(self.channel))

    def get_basetopic(self, topic):
        topic = TopicMatchers.data.sub('', topic)
        topic = TopicMatchers.event.sub('', topic)
        return topic

    def classify_topic(self, topic):
        if TopicMatchers.data.search(topic): return MessageType.DATA_CONTAINER
        if TopicMatchers.discrete.search(topic): return MessageType.DATA_DISCRETE
        if TopicMatchers.event.search(topic): return MessageType.EVENT
        if TopicMatchers.error.search(topic): return MessageType.ERROR

    def mqtt_receive(self, topic=None, payload=None, **kwargs):
        try:
            # Synchronous message processing
            #return self.process_message(topic, payload, **kwargs)

            # Asynchronous message processing
            #deferred = threads.deferToThread(self.process_message, topic, payload, **kwargs)

            # Asynchronous message processing using different thread pool
            deferred = self.thimble.process_message(topic, payload, **kwargs)

            deferred.addErrback(self.mqtt_process_error, topic, payload)
            deferred.addErrback(self.mqtt_exception, topic, payload)
            return deferred

        except Exception:
            log.failure(u'Processing MQTT message failed. topic={topic}, payload={payload}', topic=topic, payload=payload)

    def process_message(self, topic, payload, **kwargs):

        payload = payload.decode('utf-8')

        # Ignore MQTT error signalling messages.
        if topic.endswith('error.json'):
            return

        # Sanity checks: Only accept messages for the realm we are responsible for.
        if self.channel.realm and not topic.startswith(self.channel.realm):
            # log.info('Ignoring message to topic {topic}, realm={realm}', topic=topic, realm=self.channel.realm)
            return False

        # Reporting.
        log.debug(u"Processing message on topic '{topic}' with payload '{payload}'", topic=topic, payload=payload)

        # Run the decoder subsystem.
        message = self.decode_message(topic, payload)

        if not message:
            return

        # count transaction
        self.metrics.tx_count += 1

        # TODO: Re-enable for measuring packet ingress frequency.
        # Currently turned off since sending timestamps from data acquisition.
        """
        if 'time' in message:
            self.metrics.packet_time = message['time']
        else:
            self.metrics.packet_time = None
        """

        # TODO: Data enrichment machinery, e.g. for geospatial data
        # latitude/lat, longitude/long/lon/lng
        # 1. geohash => lat/lon
        # 2. postcode/city => lat/lon (forward geocoder)
        # 3. lat/lon => geohash if not geohash
        # 4. lat/lon => reverse geocoder (address information)
        # The outcome can provide additional meta information to be used by the tagging machinery below,
        # e.g. create tags from homogenized Nomatim address modulo "house_number" etc.

        # TODO: Already do the tagging enrichment machinery here(!) to
        # establish additional metadata schema for further processing, e.g. Grafana.
        # So, move the schwumms from storage handler here!
        # Sane order for Grafana template variables:
        # continent, country_code (upper), q-region, city, q-hood, road, (compound)

        # Signal the message to the downstream subsystems, e.g. InfluxDB and Grafana.
        response = self.emit_message(message)

        # MQTT error signalling
        if isinstance(response, Failure):
            self.mqtt_publish_error(response, topic, payload)

    def decode_message(self, topic, payload):

        # Compute topology information from channel topic.
        topology = self.strategy.topic_to_topology(topic)
        log.debug(u'Topology address: {topology}', topology=dict(topology))

        message = DecodedMessage()
        message.topology = topology

        # Message can be handled by one of the device-specific decoders.
        decoder_manager = DecoderManager(topology)
        if decoder_manager.probe():
            message.type = decoder_manager.info.message_type
            message.data = decoder_manager.info.decoder.decode(payload)
            return message

        # Otherwise, try to classify the channel topic by other means.
        message.type = self.classify_topic(topic)

        # a) En bloc: Multiple measurements in JSON object
        #
        # The suffixes are:
        #
        #   - data.json:        Regular
        #   - data/__json__:    Homie
        #   - loop:             WeeWX
        #   - message-json:     Deprecated
        #
        # Todo: Move specific stuff about Homie, WeeWX or Tasmota to some device-specific knowledgebase.

        if message.type == MessageType.DATA_CONTAINER:

            # Decode regular JSON container.
            message.data = json.loads(payload)

            # Required for WeeWX data
            # message.data = convert_floats(json.loads(payload))


        # b) Discrete values
        #
        # The suffixes are:
        #
        #   - data/temperature
        #   - data/humidity
        #   - ...
        #
        elif message.type == MessageType.DATA_DISCRETE:

            # Todo: Backward compat for single readings - refactor elsewhere.
            if 'slot' in topology and topology.slot.startswith('measure/'):
                topology.slot = topology.slot.replace('measure/', 'data/')

            # Single measurement as plain value; assume float
            # Convert to MessageType.DATA_CONTAINER
            if 'slot' in topology and topology.slot.startswith('data/'):
                # This is sensor data
                message.type = MessageType.DATA_CONTAINER

                # Amend topic and compute storage message from single scalar value
                name = topology.slot.replace('data/', '')
                value = float(payload)
                message.data = {name: value}

        # Set an event
        elif message.type == MessageType.EVENT:

            # This is an event
            message.type = MessageType.EVENT

            # Decode message from json format
            message.data = json.loads(payload)

        # Catch an error message
        # TODO: Signal via MQTT
        elif message.type == MessageType.ERROR:
            log.warn(u'Ignoring error message from MQTT, "{topic}" with payload "{payload}"',
                     topic=topic, payload=payload)
            return

        else:
            log.debug(u'Unknown message type on topic "{topic}" with payload "{payload}", ignoring.',
                      topic=topic, payload=payload)
            return

        return message

    def emit_message(self, message):

        # Compute storage location from topology information.
        storage_location = self.strategy.topology_to_storage(message.topology, message_type=message.type)
        log.debug(u'Storage location: {storage}', storage=dict(storage_location))

        # Store data or event.
        if message.type in (MessageType.DATA_CONTAINER, MessageType.EVENT):
            self.store_message(storage_location, message.data)

        # Provision graphing subsystem.
        if message.type == MessageType.DATA_CONTAINER:
            # TODO: Purge message from fields to be used as tags
            # Namely:
            # 'geohash',
            # 'location', 'location_id', 'location_name', 'sensor_id', 'sensor_type',
            # 'latitude', 'longitude', 'lat', 'lon'
            for graphing_subsystem in self.graphing:

                # Mix in references to each other. A bit of a hack, but okay for now :-).
                graphing_subsystem.strategy = self.strategy

                subsystem_name = graphing_subsystem.__class__.__name__
                log.debug(u'Provisioning Grafana with {name}', name=subsystem_name)
                try:
                    graphing_subsystem.provision(storage_location, message.data, topology=message.topology)

                except Exception as ex:
                    log.failure(u'Grafana provisioning failed for storage={storage}, message={message}:\n{log_failure}',
                                storage=storage_location.dump(), message=message.data,
                                level=LogLevel.error)

                    return Failure(Exception('Grafana provisioning failed'))

        return True

    def store_message(self, storage, data):
        """
        Store data to timeseries database

        :param storage: The storage location object
        :param data:    The data ready for storing
        """
        self.influx.write(storage, data)

    def mqtt_process_error(self, failure, topic, payload):
        """
        Failure handling

        :param failure: Failure object from Twisted
        :param topic:   Full MQTT topic
        :param payload: Raw MQTT payload
        """

        # Log failure
        log.failure(u'Processing MQTT message failed from topic "{topic}":\n{log_failure}', topic=topic, failure=failure, level=LogLevel.error)

        # MQTT error signalling
        self.mqtt_publish_error(failure, topic, payload)

    def mqtt_exception(self, failure, topic, payload):
        log.failure(u'Problem publishing error message:\n{log_failure}', failure=failure, level=LogLevel.warn)

    def mqtt_publish_error(self, failure, topic, payload):
        """
        Error signalling over MQTT to "error.json" topic suffix

        :param failure: Failure object from Twisted
        :param topic:   Full MQTT topic
        :param payload: Raw MQTT payload
        """

        # Compute base topic of data acquisition channel
        basetopic = self.get_basetopic(topic)
        log.debug(u'Channel base topic is {basetopic}', basetopic=basetopic)

        # Effective error reporting topic
        error_topic = basetopic + '/' + 'error.json'

        #
        error = {
            'type': str(failure.type),
            'message': failure.getErrorMessage(),
            'description': u'Error processing MQTT message "{payload}" from topic "{topic}".'.format(topic=topic, payload=payload),
            'timestamp': arrow.utcnow().format('YYYY-MM-DDTHH:mm:ssZZ'),
            #'failure': unicode(failure),
        }
        message = json.dumps(error, indent=4)

        # Publish error signal over MQTT
        #log.debug('Publishing error message to topic {topic}: {message}', topic=error_topic, message=message)
        self.mqtt_service.publish(error_topic, message)

    def process_metrics(self):

        metrics = []

        # Compute frequency of measurements
        if 'packet_time' in self.metrics and self.metrics['packet_time'] is not None:

            self.metrics.setdefault('packet_starttime', self.metrics.packet_time)

            # Convert nanos to seconds
            packet_duration = (self.metrics.packet_time - self.metrics.packet_starttime) / 1000.0 / 1000.0 / 1000.0
            packet_duration = packet_duration or self.metrics.starttime
            if packet_duration != 0:
                packet_frequency = self.metrics.tx_count / float(packet_duration)
            else:
                packet_frequency = 0.0

            metrics.append('measurements: %.02f Hz' % packet_frequency)

            # Reset for next round
            self.metrics.packet_starttime = self.metrics.packet_time

        # Compute frequency of transactions
        now = time.time()
        transaction_duration = now - self.metrics.starttime
        if transaction_duration != 0:
            transaction_frequency = self.metrics.tx_count / float(transaction_duration)
        else:
            transaction_frequency = 0.0
        metrics.append('transactions: %.02f tps' % transaction_frequency)

        # Reset for next round
        self.metrics.tx_count = 0
        self.metrics.starttime = now


        # Add information from the Twisted reactor
        pending_calls = reactor.getDelayedCalls()
        pending_count = len(pending_calls)
        #metrics.append('pending: %d' % pending_count)

        metrics_info = ', '.join(metrics)

        log.info('[{realm:12s}] {metrics_info}', realm=self.channel.realm, metrics_info=metrics_info)


class DecodedMessage:
    def __init__(self):
        self.topology = None
        self.type = None
        self.data = None
