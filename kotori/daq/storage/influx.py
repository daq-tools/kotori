# -*- coding: utf-8 -*-
# (c) 2015-2023 Andreas Motl <andreas@getkotori.org>
import requests
from copy import deepcopy
from funcy import project
from collections import OrderedDict
from twisted.logger import Logger
from influxdb.client import InfluxDBClient, InfluxDBClientError

from kotori.daq.storage.util import format_chunk

log = Logger()


class InfluxDBAdapter(object):

    def __init__(self, settings=None, database=None):

        settings = deepcopy(settings) or {}
        settings.setdefault('host', u'localhost')
        settings.setdefault('port', u'8086')
        settings.setdefault('username', u'root')
        settings.setdefault('password', u'root')
        settings.setdefault('database', database)
        settings.setdefault('pool_size', 10)

        settings.setdefault('use_udp', False)
        settings.setdefault('udp_port', u'4444')

        settings['port'] = int(settings['port'])
        settings['udp_port'] = int(settings['udp_port'])

        self.__dict__.update(**settings)

        # Bookkeeping for all databases having been touched already
        self.databases_written_once = set()

        # Knowledge about all databases to be accessed using UDP
        # TODO: Refactor to configuration setting
        self.udp_databases = [
            {'name': 'luftdaten_info', 'port': u'4445'},
        ]
        self.host_uri = u'influxdb://{host}:{port}'.format(**self.__dict__)

        log.info(u'Storage target is {uri}, pool size is {pool_size}', uri=self.host_uri, pool_size=self.pool_size)
        self.influx_client = InfluxDBClient(
            host=self.host, port=self.port,
            username=self.username, password=self.password,
            database=self.database, pool_size=self.pool_size,
            timeout=10)

        # TODO: Hold references to multiple UDP databases using mapping "self.udp_databases".
        self.influx_client_udp = None
        if settings['use_udp']:
            self.influx_client_udp = InfluxDBClient(
                host=self.host, port=self.port,
                username=self.username, password=self.password,
                use_udp=settings['use_udp'], udp_port=settings['udp_port'],
                timeout=10)

    def is_udp_database(self, name):
        for entry in self.udp_databases:
            if entry['name'] == name:
                return True
        return False

    def write(self, meta, data):

        meta_copy = deepcopy(dict(meta))
        data_copy = deepcopy(data)

        try:
            chunk = format_chunk(meta, data)

        except Exception as ex:
            log.failure(u'Could not format chunk (ex={ex_name}: {ex}): data={data}, meta={meta}',
                ex_name=ex.__class__.__name__, ex=ex, meta=meta_copy, data=data_copy)
            raise

        try:
            success = self.write_chunk(meta, chunk)
            return success

        except requests.exceptions.ConnectionError as ex:
            log.failure(u'Problem connecting to InfluxDB at {uri}: {ex}', uri=self.host_uri, ex=ex)
            raise

        except InfluxDBClientError as ex:

            if ex.code == 404 or 'database not found' in ex.content:

                log.info('Creating database "{database}"', database=meta.database)
                self.influx_client.create_database(meta.database)

                # Attempt second write
                success = self.write_chunk(meta, chunk)
                return success

                #log.failure('InfluxDBClientError: {ex}', ex=ex)

            # [0.8] ignore "409: database kotori-dev exists"
            # [0.9] ignore "database already exists"
            elif ex.code == 409 or 'database already exists' in ex.content:
                pass
            else:
                raise

    def write_chunk(self, meta, chunk):
        if self.influx_client_udp and self.is_udp_database(meta.database) and meta.database in self.databases_written_once:
            success = self.influx_client_udp.write_points([chunk], time_precision='s', database=meta.database)
        else:
            success = self.influx_client.write_points([chunk], time_precision=chunk['time_precision'], database=meta.database)
            self.databases_written_once.add(meta.database)
        if success:
            log.debug(u"Storage success: {chunk}", chunk=chunk)
        else:
            log.error(u"Storage failed:  {chunk}", chunk=chunk)
        return success

    @staticmethod
    def get_tags(data):
        return project(data, ['gateway', 'node'])


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
        value = str(value).replace('/', '_').replace('.', '_').replace('-', '_')
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
        if isinstance(payload, dict):
            message = payload.copy()
        elif isinstance(payload, list):
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

