# -*- coding: utf-8 -*-
# (c) 2020 Andreas Motl <andreas@getkotori.org>
import os
import json
import logging

import pytest
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError
from pyinfluxql import Query
from twisted.internet import threads, reactor
from twisted.internet.task import deferLater

import kotori


logger = logging.getLogger(__name__)


def boot_kotori():
    options = {
        '--config': './etc/test-mqttkit.ini',
        '--debug': True,
        '--debug-mqtt': True,
    }
    loader = kotori.boot(options)
    return loader


class InfluxWrapper:

    def __init__(self, database, measurement):
        self.database = database
        self.measurement = measurement
        self.client = self.get_client()
        self.create = None
        self.reset = None

    def get_client(self):
        # TODO: Get configuration parameters from .ini file or from runtime application.
        influx_client = InfluxDBClient(
            host='localhost',
            database=self.database,
            timeout=2)
        return influx_client

    def query(self):
        logger.info('InfluxDB: Querying database')
        expression = Query('*').from_(self.measurement) # .where(time__gte=time_begin, time__lte=time_end, **tags)
        influx_client = self.get_client()
        result = influx_client.query(expression)
        return result

    def get_first_record(self):
        return self.get_record(index=0)

    def get_record(self, index=None):
        result = self.query()

        # One measurement?
        assert len(result) == 1

        # One record.
        records = list(result[self.measurement])
        assert len(records) == 1

        # Check record.
        record = records[index]

        return record

    def make_create_db(self):
        @pytest.fixture(scope="package")
        def create():
            logger.info('InfluxDB: Creating database')
            #self.client.drop_database(self.database)
            self.client.create_database(self.database)
        return create

    def make_reset_measurement(self):

        @pytest.fixture(scope="function")
        def reset_measurement():
            logger.info('InfluxDB: Resetting database')
            # Clear out the database.
            influx = InfluxWrapper(database=self.database, measurement=self.measurement)
            influx.client.delete_series(self.database, measurement=self.measurement)
            #try:
            #except InfluxDBClientError as ex:
            #    if 'database not found: mqttkit_1_itest' not in ex.message:
            #        raise

        return reset_measurement



def sleep(secs):
    # https://gist.github.com/jhorman/891717
    return deferLater(reactor, secs, lambda: None)





def mqtt_sensor(topic, data):
    logger.info('MQTT: Submitting measurement')
    payload = json.dumps(data)
    command = "mosquitto_pub -h localhost -t '{topic}' -m '{payload}'".format(topic=topic, payload=payload)
    logger.info('Running command {}'.format(command))
    os.system(command)
