# -*- coding: utf-8 -*-
# (c) 2015-2016 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import os
from bunch import Bunch
from binascii import hexlify
from copy import deepcopy
from pkg_resources import resource_filename
from twisted.logger import Logger
from twisted.internet import reactor

from kotori.util.configuration import read_list
from kotori.daq.intercom.c import LibraryAdapter, StructRegistryByID
from kotori.daq.intercom.wamp import WampApplication, WampSession
from kotori.daq.intercom.udp import UdpBusForwarder
from kotori.daq.storage.influx import BusInfluxForwarder
from kotori.daq.graphing.grafana.manager import GrafanaManager
from kotori.vendor.lst.message import BinaryMessageAdapter

log = Logger()


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
        log.info('Starting UDPReceiver on port {}'.format(udp_port))

        # create decoder adapter
        self.messenger = setup_binary_message_adapter(self.config)

        self.run()

    def run(self):
        """
        Run forwarding component, which actually moves data between UDP and the software bus
        """
        udp_port = int(self.config['_active_']['udp_port'])
        topic = str(self.config['_active_']['wamp_topic'])

        log.info('Starting udp adapter on port "{}", publishing to topic "{}"'.format(udp_port, topic))
        reactor.listenUDP(
            udp_port,
            UdpBusForwarder(
                bus=self.bus,
                topic=topic,
                transform=[self.binary_decode, self.bus_encode],
                logger=log))

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

        # plain
        #data = self.messenger.to_dict(struct)

        # with transformation rules
        data = self.messenger.transform(struct)

        data['_name_'] = struct._name_()
        data['_hex_'] = hexlify(struct._dump_())
        # bus message should be a list of tuples to keep field order
        data_bus = list(data.items())
        return data_bus


class InfluxStorage(BusInfluxForwarder):
    """
    Receive messages from software bus and store them into InfluxDB timeseries database
    """

    # TODO: Improve parameter passing
    def __init__(self, *args, **kwargs):
        BusInfluxForwarder.__init__(self, *args, **kwargs)

        # grafana setup
        try:
            self.graphing = GrafanaManager(settings=self.config, channel=self.channel)
        except Exception as ex:
            log.failure('Error starting GrafanaManager')

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

    def on_store(self, location, data):
        # provision graphing subsystem
        try:
            self.graphing.provision(location, data)
        except Exception:
            log.failure(u'Failed provisioning Grafana')


class StorageAdapter(object):
    """
    Encapsulation for receiving messages from software bus, mungling and storing into InfluxDB
    """

    def __init__(self, bus, config):
        self.bus = bus
        self.config = config
        log.info('Starting InfluxStorage')
        # TODO: Refactor the _active_ mechanics
        topic = str(self.config['_active_']['wamp_topic'])
        channel = Bunch(
            settings = self.config['_active_']
        )
        # TODO: Improve parameter passing
        InfluxStorage(bus=self.bus, topic=topic, config=self.config, channel=channel)


class UdpSession(WampSession):
    component = UDPReceiver


class StorageSession(WampSession):
    component = StorageAdapter


def setup_binary_message_adapter(config):
    # TODO: refactor towards OO; e.g. BinaryMessageAdapterFactory

    # TODO: improve path handling
    include_path = config['_active_']['include_path']
    if not include_path.startswith('/'):
        kotori_path = resource_filename('kotori', '')
        include_path = os.path.join(kotori_path, '..', include_path)

    # build and load library
    library = LibraryAdapter.from_header(
        include_path=include_path,
        header_files=config['_active_']['header_files'].split(','))

    # register structs
    struct_registry = StructRegistryByID(library)

    # wrap into decoder adapter
    adapter = BinaryMessageAdapter(struct_registry=struct_registry)

    return adapter


def lst_boot(config, debug=False):
    # TODO: refactor towards OO; e.g. BinaryMessageApplicationFactory

    wamp_uri = str(config.wamp.uri)

    # activate/mount multiple "lst" applications
    for channel_name in read_list(config['lst']['channels']):
        log.info('Starting "lst" channel "{}"'.format(channel_name))
        channel = config[channel_name]

        config = deepcopy(config)
        config['_active_'] = channel

        WampApplication(url=wamp_uri, realm=u'lst', session_class=UdpSession, config=config).make()
        WampApplication(url=wamp_uri, realm=u'lst', session_class=StorageSession, config=config).make()
