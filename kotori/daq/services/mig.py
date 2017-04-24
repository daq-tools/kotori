# -*- coding: utf-8 -*-
# (c) 2015-2017 Andreas Motl <andreas@getkotori.org>
import time
import json
from bunch import Bunch
from kotori.thimble import Thimble
from twisted.logger import Logger, LogLevel
from twisted.internet import reactor, threads
from twisted.internet.task import LoopingCall
from twisted.application.service import MultiService
from twisted.python.threadpool import ThreadPool
from kotori.configuration import read_list
from kotori.daq.services import MultiServiceMixin
from kotori.daq.intercom.mqtt import MqttAdapter
from kotori.daq.storage.influx import InfluxDBAdapter
from kotori.io.protocol.util import convert_floats

log = Logger()

class MqttInfluxGrafanaService(MultiService, MultiServiceMixin):

    def __init__(self, channel=None, graphing=None, strategy=None):

        MultiService.__init__(self)

        self.channel = channel or Bunch(realm=None, subscriptions=[])
        self.graphing = graphing
        self.strategy = strategy

        # Mix in references to each other. A bit of a hack, but okay for now :-).
        self.graphing.strategy = self.strategy

        self.name = u'service-mig-' + self.channel.get('realm', unicode(id(self)))

    def setupService(self):
        #self.log(log.info, u'Setting up')
        self.settings = self.parent.settings

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
        self.log(log.info, u'Starting')
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

    def mqtt_receive(self, topic=None, payload=None, **kwargs):
        try:
            # Synchronous message processing
            #return self.process_message(topic, payload, **kwargs)

            # Asynchronous message processing
            #deferred = threads.deferToThread(self.process_message, topic, payload, **kwargs)

            # Asynchronous message processing using different thread pool
            deferred = self.thimble.process_message(topic, payload, **kwargs)

            deferred.addErrback(self.mqtt_receive_error, topic)
            return deferred

        except Exception:
            log.failure(u'Processing MQTT message failed. topic={topic}, payload={payload}', topic=topic, payload=payload)

    def mqtt_receive_error(self, failure, topic):
        log.failure('Error processing MQTT message from topic "{topic}": {log_failure}', topic=topic, failure=failure, level=LogLevel.error)

    def process_message(self, topic, payload, **kwargs):

        payload = payload.decode('utf-8')

        log.debug('Received message on topic "{topic}" with payload "{payload}"', topic=topic, payload=payload)

        if self.channel.realm and not topic.startswith(self.channel.realm):
            #log.info('Ignoring message to topic {topic}, realm={realm}', topic=topic, realm=self.channel.realm)
            return False

        # Compute storage address from topic
        topology = self.topic_to_topology(topic)
        log.debug(u'Topology address: {topology}', topology=dict(topology))

        message_type = None
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
        if topic.endswith('data.json') \
            or topic.endswith('data/__json__') \
            or topic.endswith('loop') \
            or topic.endswith('message-json'):

            # This is sensor data
            message_type = 'data'

            # Decode message from json format
            # Required for weeWX data
            #message = convert_floats(json.loads(payload))
            message = json.loads(payload)

        # b) Discrete values
        else:

            # TODO: Backward compat for single readings - remove!
            if 'slot' in topology and topology.slot.startswith('measure/'):
                topology.slot = topology.slot.replace('measure/', 'data/')

            # Single measurement as plain value; assume float
            if 'slot' in topology and topology.slot.startswith('data/'):

                # This is sensor data
                message_type = 'data'

                # Amend topic and compute storage message from single scalar value
                name = topology.slot.replace('data/', '')
                value = float(payload)
                message = {name: value}


        # Set an event
        if topic.endswith('event.json'):

            # This is an event
            message_type = 'event'

            # Decode message from json format
            message = json.loads(payload)


        if not message_type:
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

        storage_location = self.topology_to_storage(topology)
        log.debug(u'Storage location: {storage}', storage=dict(storage_location))

        # store data
        self.store_message(storage_location, message)

        # provision graphing subsystem
        if message_type == 'data':
            self.graphing.provision(storage_location, message, topology=topology)

        return True


    def store_message(self, storage, data):
        self.influx.write(storage, data)

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
