# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import json
from kotori.daq.storage.influx import InfluxDBAdapter
from bunch import Bunch
from twisted.logger import Logger
from kotori.hiveeyes.mqtt_adapter import HiveeyesMqttAdapter

logger = Logger()

class HiveeyesApplication(object):

    def __init__(self, broker_host, broker_port, influxdb_host):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.influxdb_host = influxdb_host

        self.subscriptions = ['hiveeyes/#']

        self.mqtt = HiveeyesMqttAdapter(
            broker_host=self.broker_host, broker_port=self.broker_port,
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
            'database': '.'.join(parts[0:2]),
            'series': '.'.join(parts[2:4]),
        })
        print 'address:', address
        return address

    def mungle_data(self, data):
        del data['network_id']
        del data['gateway_id']
        del data['node_id']
        return data

    def store_message(self, database, series, data):
        influx = InfluxDBAdapter(host=self.influxdb_host, database=database)
        influx.write(series, data)


def hiveeyes_boot(broker_host='localhost', broker_port=1883, influxdb_host='localhost', debug=False):
    ha = HiveeyesApplication(broker_host=broker_host, broker_port=broker_port, influxdb_host=influxdb_host)
