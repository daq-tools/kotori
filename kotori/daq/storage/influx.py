# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import requests
from twisted.internet import reactor
from twisted.logger import Logger
from kotori.util import slm

logger = Logger()

class InfluxDBAdapter(object):

    def __init__(self, host='localhost', port=8086, version='0.8', username='root', password='root', database='kotori_dev'):
        self.host = host
        self.port = port
        self.version = version
        self.username = username
        self.password = password
        self.database = database
        self.influx = None

        self.connected = False
        self.connect()

    def connect(self):

        if self.connected:
            return True

        if self.version == '0.8':
            from influxdb.influxdb08.client import InfluxDBClient, InfluxDBClientError

        elif self.version == '0.9':
            from influxdb.client import InfluxDBClient, InfluxDBClientError

        else:
            raise ValueError('Unknown InfluxDB protocol version "{}"'.format(self.version))

        self.influx = InfluxDBClient(
            host=self.host, port=self.port,
            username=self.username, password=self.password,
            database=self.database)

        try:
            self.influx.create_database(self.database)

        except requests.exceptions.ConnectionError as ex:
            self.connected = False
            logger.error('InfluxDB network error: {}'.format(slm(ex)))
            return False

        except InfluxDBClientError as ex:
            # [0.8] ignore "409: database kotori-dev exists"
            # [0.9] ignore "database already exists"
            if ex.code == 409 or ex.message == 'database already exists':
                pass
            else:
                self.connected = False
                logger.error('InfluxDBClientError: {}'.format(slm(ex)))
                return False

        self.connected = True
        return True


    def write_real(self, chunk):
        """
        format 0.8::

            [
                {
                    "name": "telemetry",
                    "columns": ["value"],
                    "points": [
                        [0.42]
                    ]
                }
            ]

        format 0.9::

            [
                {
                    "measurement": "hiveeyes_100",
                    "tags": {
                        "host": "server01",
                        "region": "europe"
                    },
                    "time": "2015-10-17T19:30:00Z",
                    "fields": {
                        "value": 0.42
                    }
                }
            ]

        """

        try:
            if self.version == '0.8':
                pass

            elif self.version == '0.9':
                chunk = self.v08_to_09(chunk)

            else:
                raise ValueError('Unknown InfluxDB protocol version "{}"'.format(self.version))

            success = self.influx.write_points([chunk])
            if success:
                logger.info("Storing measurement succeeded: {}".format(slm(chunk)))
            else:
                logger.error("Storing measurement failed: {}".format(slm(chunk)))
            return success

        except requests.exceptions.ConnectionError as ex:
            logger.error('InfluxDB network error: {}'.format(slm(ex)))


    def v08_to_09(self, chunk08):
        chunk09 = {
            "measurement": chunk08["name"],
            #"tags": {
            #    "host": "server01",
            #    "region": "us-west"
            #},
            #"time": "2009-11-10T23:00:00Z",  # TODO: use timestamp from downstream chunk
            "fields": dict(zip(chunk08["columns"], chunk08["points"][0])),
        }
        logger.debug('chunk09: {}'.format(slm(chunk09)))
        return chunk09

    def write(self, name, data):
        columns = data.keys()
        points = data.values()
        return self.write_points(name, columns, points)

    def write_points(self, name, columns, points):
        chunk = {
                    "name": name,
                    "columns": columns,
                    "points": [points],
                }
        return self.write_real(chunk)
