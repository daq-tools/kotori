# -*- coding: utf-8 -*-
# (c) 2015-2018 Andreas Motl <andreas@getkotori.org>
import re
import time
import json
import arrow
from bunch import Bunch
from twisted.logger import Logger, LogLevel
from twisted.internet import reactor, threads
from twisted.internet.task import LoopingCall
from twisted.application.service import MultiService, Service
from twisted.python.failure import Failure
from twisted.python.threadpool import ThreadPool
from kotori.configuration import read_list
from kotori.daq.services.schema import MessageType, TopicMatchers
from kotori.daq.services import MultiServiceMixin
from kotori.daq.intercom.mqtt import MqttAdapter
from kotori.daq.storage.influx import InfluxDBAdapter
from kotori.io.protocol.util import convert_floats
from kotori.thimble import Thimble

log = Logger()


class MqttInfluxGrafanaService(MultiService, MultiServiceMixin):

    def __init__(self, channel=None, graphing=None, strategy=None):

        MultiService.__init__(self)

        # TODO: Make subsystems dynamic
        self.subsystems = ['channel', 'graphing', 'strategy']
        self.channel = channel or Bunch(realm=None, subscriptions=[])
        self.graphing = graphing
        self.strategy = strategy

        # Mix in references to each other. A bit of a hack, but okay for now :-).
        self.graphing.strategy = self.strategy

        self.name = u'service-mig-' + self.channel.get('realm', unicode(id(self)))

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
        level('{prefix} {class_name}. name={name}, channel={channel}',
            prefix=prefix, class_name=self.__class__.__name__, name=self.name, channel=dict(self.channel))

    def topic_to_topology(self, topic):
        return self.strategy.topic_to_topology(topic)

    def topology_to_storage(self, topology):
        return self.strategy.topology_to_storage(topology)

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

        # Ignore MQTT error signalling messages
        if topic.endswith('error.json'):
            return

        if self.channel.realm and not topic.startswith(self.channel.realm):
            #log.info('Ignoring message to topic {topic}, realm={realm}', topic=topic, realm=self.channel.realm)
            return False

        log.debug('Processing message on topic "{topic}" with payload "{payload}"', topic=topic, payload=payload)

        # Compute storage address from topic
        topology = self.topic_to_topology(topic)
        log.debug(u'Topology address: {topology}', topology=dict(topology))

        message_type = self.classify_topic(topic)
        message = None

        # a) En bloc: Multiple measurements in JSON object
        #
        # The suffixes are:
        #
        #   - data.json:        Regular
        #   - data/__json__:    Homie
        #   - loop:             WeeWX           (TODO: Move to specific vendor configuration.)
        #   - message-json:     Deprecated
        #
        if message_type == MessageType.DATA_CONTAINER:

            # Decode message from json format
            # Required for weeWX data
            #message = convert_floats(json.loads(payload))
            message = json.loads(payload)

        # b) Discrete values
        #
        # The suffixes are:
        #
        #   - data/temperature
        #   - data/humidity
        #   - ...
        #
        elif message_type == MessageType.DATA_DISCRETE:

            # TODO: Backward compat for single readings - remove!
            if 'slot' in topology and topology.slot.startswith('measure/'):
                topology.slot = topology.slot.replace('measure/', 'data/')

            # Single measurement as plain value; assume float
            # Convert to MessageType.DATA_CONTAINER
            if 'slot' in topology and topology.slot.startswith('data/'):

                # This is sensor data
                message_type = MessageType.DATA_CONTAINER

                # Amend topic and compute storage message from single scalar value
                name = topology.slot.replace('data/', '')
                value = float(payload)
                message = {name: value}


        # Set an event
        elif message_type == MessageType.EVENT:

            # This is an event
            message_type = MessageType.EVENT

            # Decode message from json format
            message = json.loads(payload)

        # Catch an error message
        elif message_type == MessageType.ERROR:
            log.debug('Ignoring error message from MQTT, "{topic}" with payload "{payload}"', topic=topic, payload=payload)
            return

        else:
            log.debug('Unknown message type on topic "{topic}" with payload "{payload}"', topic=topic, payload=payload)
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

        # Compute storage location
        storage_location = self.topology_to_storage(topology)
        log.debug(u'Storage location: {storage}', storage=dict(storage_location))

        # Store data or event
        if message_type in (MessageType.DATA_CONTAINER, MessageType.EVENT):
            self.store_message(storage_location, message)

        # Provision graphing subsystem
        if message_type == MessageType.DATA_CONTAINER:
            # TODO: Purge message from fields to be used as tags
            # Namely:
            # 'geohash',
            # 'location', 'location_id', 'location_name', 'sensor_id', 'sensor_type',
            # 'latitude', 'longitude', 'lat', 'lon'
            try:
                self.graphing.provision(storage_location, message, topology=topology)
            except Exception as ex:
                log.failure('Grafana provisioning failed for storage={storage}, message={message}:\n{log_failure}',
                            storage=storage_location, message=message,
                            level=LogLevel.error)

                # MQTT error signalling
                failure = Failure()
                self.mqtt_publish_error(failure, topic, payload)

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
        log.failure('Processing MQTT message failed from topic "{topic}":\n{log_failure}', topic=topic, failure=failure, level=LogLevel.error)

        # MQTT error signalling
        self.mqtt_publish_error(failure, topic, payload)

    def mqtt_exception(self, failure, topic, payload):
        log.failure('Problem publishing error message:\n{log_failure}', failure=failure, level=LogLevel.warn)

    def mqtt_publish_error(self, failure, topic, payload):
        """
        Error signalling over MQTT to "error.json" topic suffix

        :param failure: Failure object from Twisted
        :param topic:   Full MQTT topic
        :param payload: Raw MQTT payload
        """

        # Compute base topic of data acquisition channel
        basetopic = self.get_basetopic(topic)
        log.debug('Channel base topic is {basetopic}', basetopic=basetopic)

        # Effective error reporting topic
        error_topic = basetopic + '/' + 'error.json'

        #
        error = {
            'type': unicode(failure.type),
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
