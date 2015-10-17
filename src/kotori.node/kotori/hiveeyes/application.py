# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import json
from bunch import Bunch
from twisted.logger import Logger
from kotori.hiveeyes.mqtt_adapter import HiveeyesMqttAdapter
from kotori.daq.storage.influx import InfluxDBAdapter

logger = Logger()

class HiveeyesApplication(object):

    def __init__(self, config):

        if not config.has_option('mqtt', 'host'):
            config.set('mqtt', 'host', 'localhost')

        if not config.has_option('mqtt', 'port'):
            config.set('mqtt', 'port', '1883')

        self.config = config

        self.subscriptions = ['hiveeyes/#']

        self.mqtt = HiveeyesMqttAdapter(
            broker_host=self.config.get('mqtt', 'host'), broker_port=int(self.config.get('mqtt', 'port')),
            callback=self.mqtt_receive,
            subscriptions=self.subscriptions)

    def mqtt_receive(self, topic, payload, *args):

        payload = payload.decode('utf-8')

        msg = 'MQTT receive: topic={}, payload={}'.format(topic, payload)
        print msg
        #logger.info(msg) # croaks on json payloads

        if topic.startswith('hiveeyes') and topic.endswith('message-json'):

            # compute storage address from topic
            db_address = self.storage_address_from_topic(topic)

            # decode data from json format
            data = json.loads(payload)

            # remove some non-data fields
            data = self.mungle_data(data)

            # store data
            self.store_message(db_address.database, db_address.series, data)

    def storage_address_from_topic(self, topic):
        parts = topic.split('/')
        address = Bunch({
            # use "_" as database name fragment separator: "/" does not work in InfluxDB 0.8, "." does not work in InfluxDB 0.9
            'database': '_'.join(parts[0:2]),
            'series': '.'.join(parts[2:4]),
        })
        print 'database address:', dict(address)
        return address

    def mungle_data(self, data):
        del data['network_id']
        del data['gateway_id']
        del data['node_id']
        return data

    def store_message(self, database, series, data):
        influx = InfluxDBAdapter(
            version  = self.config.get('influxdb', 'version'),
            host     = self.config.get('influxdb', 'host'),
            username = self.config.get('influxdb', 'username'),
            password = self.config.get('influxdb', 'password'),
            database = database)
        influx.write(series, data)


def hiveeyes_boot(config, debug=False):
    ha = HiveeyesApplication(config)
