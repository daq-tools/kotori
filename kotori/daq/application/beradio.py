# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import json
from kotori.errors import last_error_and_traceback
from twisted.logger import Logger
from kotori.daq.storage.influx import InfluxDBAdapter
from kotori.daq.intercom.mqtt_adapter import MqttAdapter
from kotori.util import slm

logger = Logger()

class BERadioNetworkApplication(object):

    def __init__(self, config):
        self.config = config

        self.realm = 'beradio'
        self.subscriptions = []

        if not config.has_option('mqtt', 'host'):
            config.set('mqtt', 'host', 'localhost')

        if not config.has_option('mqtt', 'port'):
            config.set('mqtt', 'port', '1883')

        if not config.has_option('mqtt', 'debug'):
            config.set('mqtt', 'debug', 'false')

    def setup(self):

        self.mqtt = MqttAdapter(
            broker_host   = self.config.get('mqtt', 'host'),
            broker_port   = int(self.config.get('mqtt', 'port')),
            callback      = self.mqtt_receive,
            subscriptions = self.subscriptions)

    def topic_to_topology(self, topic):
        raise NotImplementedError()

    def topology_to_database(self, topology):
        raise NotImplementedError()

    def mqtt_receive(self, topic, payload, *args):
        try:
            return self.process_message(topic, payload, *args)
        except Exception as ex:
            logger.error('Processing MQTT message failed: {}\n{}'.format(ex, slm(last_error_and_traceback())))

    def process_message(self, topic, payload, *args):

        payload = payload.decode('utf-8')

        msg = 'MQTT receive: topic={}, payload={}'.format(topic, payload)
        logger.debug(slm(msg))

        if topic.startswith(self.realm) and topic.endswith('message-json'):

            # compute storage address from topic
            topology = self.topic_to_topology(topic)
            logger.info('Topology address: {}'.format(slm(dict(topology))))

            storage = self.topology_to_database(topology)
            logger.info('Storage address:  {}'.format(slm(dict(storage))))

            # decode message from json format
            message = json.loads(payload)

            # store data
            self.store_message(storage.database, storage.series, message)

            # provision graphing subsystem
            self.graphing.provision(storage.database, storage.series, message, topology=topology)

    def store_message(self, database, series, data):

        if not self.config.has_option('influxdb', 'port'):
            self.config.set('influxdb', 'port', '8086')

        influx = InfluxDBAdapter(
            version  = self.config.get('influxdb', 'version'),
            host     = self.config.get('influxdb', 'host'),
            port     = int(self.config.get('influxdb', 'port')),
            username = self.config.get('influxdb', 'username'),
            password = self.config.get('influxdb', 'password'),
            database = database)

        influx.write(series, data)
