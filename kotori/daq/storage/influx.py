# -*- coding: utf-8 -*-
# (c) 2015-2017 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import types
import requests
from funcy import project
from collections import OrderedDict
from twisted.logger import Logger
from influxdb.client import InfluxDBClient, InfluxDBClientError
from kotori.io.protocol.util import parse_timestamp, is_number

log = Logger()

class InfluxDBAdapter(object):

    databases_created = []

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

        log.debug(u'Storage target is influxdb://{host}:{port}', **self.__dict__)
        self.influx = InfluxDBClient(
            host=self.host, port=self.port,
            username=self.username, password=self.password,
            database=self.database)

        self.connected = True

        # Run "CREATE DATABASE" only once
        if self.database in self.databases_created:
            return True

        try:
            self.influx.create_database(self.database)
            self.databases_created.append(self.database)

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

        return True


    def write(self, meta, data):
        try:
            chunk = self.format_chunk(meta, data)
            success = self.influx.write_points([chunk], time_precision=chunk['time_precision'])
            if success:
                log.debug(u"Storage success: {chunk}", chunk=chunk)
            else:
                log.error(u"Storage failed:  {chunk}", chunk=chunk)
            return success

        except requests.exceptions.ConnectionError:
            log.failure(u'InfluxDB connection error')

        except ValueError as ex:
            log.failure(u'Could not format chunk or write data (ex={ex}): data={data}, meta={meta}',
                ex=ex, meta=dict(meta), data=data)

    @staticmethod
    def get_tags(data):
        return project(data, ['gateway', 'node'])

    def format_chunk(self, meta, data):
        """
        Format for InfluxDB >= 0.9::
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
        """

        chunk = {
            "measurement": meta['measurement'],
            "tags": {},
        }

        """
        if "gateway" in meta:
            chunk["tags"]["gateway"] = meta["gateway"]

        if "node" in meta:
            chunk["tags"]["node"]    = meta["node"]
        """

        # Extract timestamp field from data
        chunk['time_precision'] = 'n'
        for time_field in ['time', 'dateTime']:
            if time_field in data:

                if data[time_field]:
                    chunk['time'] = data[time_field]
                    if is_number(chunk['time']):
                        chunk['time'] = int(data[time_field])

                # WeeWX. TODO: Move to specific vendor configuration.
                if time_field == 'dateTime':
                    chunk['time_precision'] = 's'

                del data[time_field]


        # TODO: Maybe do this at data acquisition / transformation time, not here.
        if 'time' in chunk:
            chunk['time'] = parse_timestamp(chunk['time'])

        """
        Prevent errors like
        ERROR: InfluxDBClientError: 400:
                       write failed: field type conflict:
                       input field "pitch" on measurement "01_position" is type float64, already exists as type integer
        """
        self.data_to_float(data)

        chunk["fields"] = data

        return chunk

    def data_to_float(self, data):
        for key, value in data.iteritems():

            # Sanity checks
            if type(value) in types.StringTypes:
                continue

            if value is None:
                data[key] = None
                continue

            # Convert to float
            try:
                data[key] = float(value)
            except (TypeError, ValueError) as ex:
                log.warn(u'Measurement "{key}: {value}" float conversion failed: {ex}', key=key, value=value, ex=ex)


class BusInfluxForwarder(object):
    """
    Generic software bus -> influxdb forwarder based on prototypic implementation at HiveEyes
    TODO: Generalize and refactor
    """

    # TODO: Improve parameter passing
    def __init__(self, bus, topic, config, channel):
        self.bus = bus
        self.topic = topic
        self.config = config
        self.channel = channel

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

        log.debug('Bus receive: topic={topic}, payload={payload}', topic=topic, payload=payload)

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
        log.debug('Storage location: {storage_location}', storage_location=dict(storage_location))

        # store data
        self.store_message(storage_location, message)


    def storage_location(self, data):
        raise NotImplementedError()

    def store_encode(self, data):
        return data

    def store_message(self, location, data):

        data = self.store_encode(data)

        influx = InfluxDBAdapter(
            settings = self.config['influxdb'],
            database = location.database)

        outcome = influx.write(location, data)
        log.debug('Store outcome: {outcome}', outcome=outcome)

        self.on_store(location, data)

    def on_store(self, location, data):
        pass

