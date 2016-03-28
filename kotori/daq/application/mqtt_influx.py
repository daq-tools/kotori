# -*- coding: utf-8 -*-
# (c) 2015-2016 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import json
from pprint import pprint
import time
from bunch import Bunch
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from twisted.logger import Logger
from kotori.daq.intercom.mqtt_adapter import MqttAdapter
from kotori.daq.storage.influx import InfluxDBAdapter

log = Logger()

class MqttInfluxApplication(object):

    def __init__(self, config):
        self.config = config

        self.realm = None
        self.subscriptions = []

        # Configure metrics to be collected each X seconds
        self.metrics = Bunch(tx_count=0, starttime=time.time(), interval=2)

        # MQTT setting defaults
        config.mqtt.setdefault('host', u'localhost')
        config.mqtt.setdefault('port', u'1883')
        config.mqtt.setdefault('debug', u'false')

    def setup(self):

        metrics_twingo = LoopingCall(self.process_metrics)
        metrics_twingo.start(self.metrics.interval, now=True)

        self.mqtt = MqttAdapter(
            broker_host   = self.config.mqtt.host,
            broker_port   = int(self.config.mqtt.port),
            callback      = self.mqtt_receive,
            subscriptions = self.subscriptions)

    def topic_to_topology(self, topic):
        raise NotImplementedError()

    def topology_to_database(self, topology):
        raise NotImplementedError()

    def mqtt_receive(self, topic, payload, *args):
        try:
            return self.process_message(topic, payload, *args)
        except Exception:
            log.failure(u'Processing MQTT message failed')

    def process_message(self, topic, payload, *args):

        payload = payload.decode('utf-8')

        log.debug('Received message on topic "{topic}" with payload "{payload}"', topic=topic, payload=payload)

        if self.realm and not topic.startswith(self.realm):
            log.info('Ignoring message to topic {topic}', topic=topic)
            return

        message_valid = False

        # entry point for multiple measurements in json object
        if topic.endswith('message-json'):
            # decode message from json format
            message = json.loads(payload)
            message_valid = True

        # entry point for single measurement as plain value; assume float
        if 'measure/' in topic:

            # compute storage message from single scalar value
            name  = topology.kind.replace('measure/', '')
            value = float(payload)
            message = {name: value}

            message_valid = True

        if not message_valid:
            return

        # count transaction
        self.metrics.tx_count += 1
        if 'time' in message:
            self.metrics.packet_time = message['time']
        else:
            self.metrics.packet_time = None

        # compute storage address from topic
        topology = self.topic_to_topology(topic)
        log.debug(u'Topology address: {topology}', topology=dict(topology))

        storage = self.topology_to_database(topology)
        log.debug(u'Storage address: {storage}', storage=dict(storage))

        # store data
        self.store_message(storage.database, storage.series, message)

        # provision graphing subsystem
        self.graphing.provision(storage.database, storage.series, message, topology=topology)


    def store_message(self, database, series, data):
        influx = InfluxDBAdapter(
            settings = self.config.influxdb,
            database = database)

        influx.write(series, data)


    def process_metrics(self):

        metrics = []

        # Compute frequency of measurements
        if 'packet_time' in self.metrics:

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

        log.info(metrics_info)
