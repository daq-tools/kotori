# -*- coding: utf-8 -*-
# (c) 2015-2021 Andreas Motl <andreas@getkotori.org>
import requests
from copy import deepcopy
from funcy import project
from collections import OrderedDict
from twisted.logger import Logger
from influxdb.client import InfluxDBClient, InfluxDBClientError
from kotori.io.protocol.util import parse_timestamp, is_number, convert_floats

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

        # Bookeeping for all databases having been touched already
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
            chunk = self.format_chunk(meta, data)

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

            if ex.code == 404 or ex.message == 'database not found':

                log.info('Creating database "{database}"', database=meta.database)
                self.influx_client.create_database(meta.database)

                # Attempt second write
                success = self.write_chunk(meta, chunk)
                return success

                #log.failure('InfluxDBClientError: {ex}', ex=ex)

            # [0.8] ignore "409: database kotori-dev exists"
            # [0.9] ignore "database already exists"
            elif ex.code == 409 or ex.message == 'database already exists':
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

        assert isinstance(data, dict), 'Data payload is not a dictionary'

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

        # TODO: Refactor to some knowledgebase component.
        time_field_candidates = [
            'time',         # Vanilla
            'datetime',     # Vanilla
            'Time',         # Tasmota
            'dateTime',     # WeeWX
            'timestamp',    # Contrib
        ]

        # Extract timestamp field from data
        chunk['time_precision'] = 'n'
        # FIXME: Unify with ``kotori.io.protocol.http.data_acquisition()``.
        for time_field in time_field_candidates:
            if time_field in data:

                # WeeWX. TODO: Move to specific vendor configuration.
                # Disabled in favor of precision detection heuristic.
                #if time_field == 'dateTime':
                #    chunk['time_precision'] = 's'

                # Process timestamp field.
                if data[time_field]:

                    # Decode timestamp.
                    chunk['time'] = data[time_field]
                    if is_number(chunk['time']):
                        chunk['time'] = int(float(chunk['time']))

                    # Remove timestamp from data payload.
                    del data[time_field]

                    # If we found a timestamp field already,
                    # don't look out for more.
                    break

        # Extract geohash from data. Finally, thanks Rich!
        # TODO: Also precompute geohash with 3-4 different zoomlevels and add them as tags
        if "geohash" in data:
            chunk["tags"]["geohash"] = data["geohash"]
            del data['geohash']

        if "latitude" in data and "longitude" in data:
            chunk["tags"]["latitude"] = data["latitude"]
            chunk["tags"]["longitude"] = data["longitude"]
            del data['latitude']
            del data['longitude']

        # Extract more information specific to luftdaten.info
        for field in ['location', 'location_id', 'location_name', 'sensor_id', 'sensor_type']:
            if field in data:
                chunk["tags"][field] = data[field]
                del data[field]

        # TODO: Maybe do this at data acquisition / transformation time, not here.
        if 'time' in chunk:
            timestamp = chunk['time'] = parse_timestamp(chunk['time'])

            # Heuristically compute timestamp precision
            if isinstance(timestamp, int):
                if timestamp >= 1e17 or timestamp <= -1e17:
                    time_precision = 'n'
                elif timestamp >= 1e14 or timestamp <= -1e14:
                    time_precision = 'u'
                elif timestamp >= 1e11 or timestamp <= -1e11:
                    time_precision = 'ms'

                # FIXME: Is this a reasonable default?
                else:
                    time_precision = 's'

                chunk['time_precision'] = time_precision

            """
            # FIXME: Breaks CSV data acquisition. Why?
            if isinstance(chunk['time'], datetime.datetime):
                if chunk['time'].microsecond == 0:
                    chunk['time_precision'] = 's'
            """

        """
        Prevent errors like
        ERROR: InfluxDBClientError: 400:
                       write failed: field type conflict:
                       input field "pitch" on measurement "01_position" is type float64, already exists as type integer
        """
        self.data_to_float(data)

        assert data, 'Data payload is empty'

        chunk["fields"] = data

        return chunk

    def data_to_float(self, data):
        return convert_floats(data)

        for key, value in data.items():

            # Sanity checks
            if isinstance(value, str):
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

