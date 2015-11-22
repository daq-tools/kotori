# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
from bunch import Bunch
from binascii import hexlify
from copy import deepcopy
from twisted.logger import Logger
from twisted.internet import reactor
from kotori.util import slm, configparser_to_dict
from kotori.errors import traceback_get_exception, last_error_and_traceback
from kotori.daq.intercom.c import LibraryAdapter, StructRegistryByID
from kotori.daq.intercom.wamp import WampApplication, WampSession
from kotori.daq.intercom.udp import UdpBusForwarder
from kotori.daq.storage.influx import BusInfluxForwarder
from kotori.daq.graphing.grafana import GrafanaManager
from kotori.vendor.lst.message import BinaryMessageAdapter

logger = Logger()

class UDPReceiver(object):
    """
    - Receive binary messages via UDP
    - Decode using information from ``h2m_struct.h``
    - Publish decoded messages to software bus in appropriate format
    """

    def __init__(self, bus, config):
        """
        - Initialize UDP receiver with software bus and configuration
        - Create decoder object from appropriate C/C++ header file
        """
        self.bus = bus
        self.config = config

        udp_port = int(self.config['_active_']['udp_port'])
        logger.info('Starting UDPReceiver on port {}'.format(udp_port))

        # create decoder adapter
        self.messenger = setup_binary_message_adapter(self.config)

        self.run()

    def run(self):
        """
        Run forwarding component, which actually moves data between UDP and the software bus
        """
        udp_port = int(self.config['_active_']['udp_port'])
        topic = unicode(self.config['_active_']['wamp_topic'])

        logger.info('Starting udp adapter on port "{}", publishing to topic "{}"'.format(udp_port, topic))
        reactor.listenUDP(
            udp_port,
            UdpBusForwarder(
                bus=self.bus,
                topic=topic,
                transform=[self.binary_decode, self.bus_encode]))

    def binary_decode(self, payload):
        """
        Decode binary message with information from C/C++ header file
        """
        struct = self.messenger.decode(payload)
        #self.messenger.pprint(struct)
        return struct

    def bus_encode(self, struct):
        """
        Mungle decoded message before publishing to software bus, add two more fields:
        - ``_name_``: name of the struct
        - ``_hex_``:  raw message payload encoded in hex
        """
        data = self.messenger.to_dict(struct)
        data['_name_'] = struct._name_()
        data['_hex_'] = hexlify(struct._dump_())
        # bus message should be a list of tuples to keep field order
        data_bus = data.items()
        return data_bus


class InfluxStorage(BusInfluxForwarder):
    """
    Receive messages from software bus and store them into InfluxDB timeseries database
    """

    def __init__(self, *args, **kwargs):
        BusInfluxForwarder.__init__(self, *args, **kwargs)

        # grafana setup
        try:
            self.graphing = GrafanaManager(self.config)
        except Exception as ex:
            logger.error(slm("{ex}, args={args!s}\n{details}\n{traceback}".format(
                ex=ex, args=args, details=traceback_get_exception(), traceback=last_error_and_traceback())))

    def storage_location(self, data):
        """
        Compute storage location (database- and timeseries-names) from message information
        """
        sanitize = self.sanitize_db_identifier
        location = Bunch({
            'database': sanitize(self.topic),
            'series':   '{:02d}_{}'.format(data['ID'], sanitize(data['_name_'].replace('struct_', ''))),
        })
        return location

    def store_encode(self, data):
        """
        Filter designated fields from message payload before storing into database
        """
        blacklist_full  = ['_name_', '_hex_', 'ID', 'length', 'ck']
        blacklist_medium  = ['_name_', 'ID', 'length', 'ck']
        blacklist_minor = ['_name_', 'ID']
        blacklist = blacklist_medium
        for entry in blacklist:
            if entry in data:
                del data[entry]
        return data

    def on_store(self, database, series, data):
        # provision graphing subsystem
        self.graphing.provision(database, series, data)


class StorageAdapter(object):
    """
    Encapsulation for receiving messages from software bus, mungling and storing into InfluxDB
    """

    def __init__(self, bus, config):
        self.bus = bus
        self.config = config
        logger.info('Starting InfluxStorage')
        topic = unicode(self.config['_active_']['wamp_topic'])
        InfluxStorage(bus=self.bus, topic=topic, config=self.config)


class UdpSession(WampSession):
    component = UDPReceiver

class StorageSession(WampSession):
    component = StorageAdapter


def setup_binary_message_adapter(config):
    # TODO: refactor towards OO; e.g. BinaryMessageAdapterFactory

    # build and load library
    library = LibraryAdapter.from_header(
        include_path=config['_active_']['include_path'],
        header_files=config['_active_']['header_files'].split(','))

    # register structs
    struct_registry = StructRegistryByID(library)

    # wrap into decoder adapter
    adapter = BinaryMessageAdapter(struct_registry=struct_registry)

    return adapter


def lst_boot(config, debug=False):
    # TODO: refactor towards OO; e.g. BinaryMessageApplicationFactory

    wamp_uri = unicode(config.get('wamp', 'listen'))

    # serialize section-based ConfigParser contents into nested dict
    config = configparser_to_dict(config)

    # activate/mount multiple "lst" applications
    for application_name in config['lst']['applications'].split(','):
        logger.info('Starting "lst" application "{}"'.format(application_name))
        application = config[application_name]

        config = deepcopy(config)
        config['_active_'] = application

        WampApplication(url=wamp_uri, realm=u'lst', session_class=UdpSession, config=config).make()
        WampApplication(url=wamp_uri, realm=u'lst', session_class=StorageSession, config=config).make()