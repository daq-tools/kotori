# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import types
import requests
from collections import OrderedDict
from twisted.logger import Logger

log = Logger()

class InfluxDBAdapter(object):

    def __init__(self, settings=None, database='kotori_develop'):

        settings = settings or {}
        settings.setdefault('host', u'localhost')
        settings.setdefault('port', u'8086')
        settings.setdefault('version', u'0.9')
        settings.setdefault('username', u'root')
        settings.setdefault('password', u'root')
        settings['port'] = int(settings['port'])

        self.__dict__.update(**settings)
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

        log.debug(u'Storage target is influxdb://{host}:{port}', **self.__dict__)
        self.influx = InfluxDBClient(
            host=self.host, port=self.port,
            username=self.username, password=self.password,
            database=self.database)

        # TODO: Run "CREATE DATABASE only once"
        try:
            self.influx.create_database(self.database)

        except requests.exceptions.ConnectionError as ex:
            self.connected = False
            log.failure(u'InfluxDB network error')
            return False

        except InfluxDBClientError as ex:
            # [0.8] ignore "409: database kotori-dev exists"
            # [0.9] ignore "database already exists"
            if ex.code == 409 or ex.message == 'database already exists':
                pass
            else:
                self.connected = False
                log.failure(u'InfluxDBClientError')
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

            """
            Prevent errors like
            ERROR: InfluxDBClientError: 400:
                           write failed: field type conflict:
                           input field "pitch" on measurement "01_position" is type float64, already exists as type integer
            """
            self.chunk_to_float(chunk)

            success = self.influx.write_points([chunk], time_precision='n')
            if success:
                log.debug(u"Storage success: {chunk}", chunk=chunk)
            else:
                log.error(u"Storage failed:  {chunk}", chunk=chunk)
            return success

        except requests.exceptions.ConnectionError:
            log.failure(u'InfluxDB network error')


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
        #log.debug('chunk09: {chunk09}', chunk09=chunk09)
        return chunk09

    def chunk_to_float(self, chunk):
        fields = chunk['fields']
        for key, value in fields.iteritems():
            if type(value) in types.StringTypes:
                continue
            try:
                fields[key] = float(value)
            except ValueError:
                pass


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


class BusInfluxForwarder(object):
    """
    Generic software bus -> influxdb forwarder based on prototypic implementation at HiveEyes
    TODO: Generalize and refactor
    """

    def __init__(self, bus, topic, config):
        self.bus = bus
        self.topic = topic
        self.config = config

        self.bus.subscribe(self.bus_receive, self.topic)


    def topic_to_topology(self, topic):
        raise NotImplementedError()

    @staticmethod
    def sanitize_db_identifier(value):
        value = unicode(value).replace('/', '_').replace('.', '_').replace('-', '_')
        return value

    def bus_receive(self, payload):
        try:
            return self.process_message(self.topic, payload)
        except Exception:
            log.failure(u'Processing bus message failed')

    def process_message(self, topic, payload, *args):

        log.info('Bus receive: topic={topic}, payload={payload}', topic=topic, payload=payload)

        # TODO: filter by realm/topic

        # decode message
        if type(payload) is types.DictionaryType:
            message = payload.copy()
        elif type(payload) is types.ListType:
            message = OrderedDict(payload)
        else:
            raise TypeError('Unable to handle data type "{}" from bus'.format(type(payload)))

        # compute storage location from topic and message
        storage_location = self.storage_location(message)
        log.info('Storage location:  {storage_location}', storage_location=storage_location)

        # store data
        self.store_message(storage_location.database, storage_location.series, message)


    def storage_location(self, data):
        raise NotImplementedError()

    def store_encode(self, data):
        return data

    def store_message(self, database, series, data):

        data = self.store_encode(data)

        influx = InfluxDBAdapter(
            version  = self.config['influxdb']['version'],
            host     = self.config['influxdb']['host'],
            port     = int(self.config['influxdb'].get('port', '8086')),
            username = self.config['influxdb']['username'],
            password = self.config['influxdb']['password'],
            database = database)

        influx.write(series, data)

        self.on_store(database, series, data)

    def on_store(self, database, series, data):
        pass

