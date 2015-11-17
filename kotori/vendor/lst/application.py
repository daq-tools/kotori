# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
from bunch import Bunch
from binascii import hexlify
from twisted.logger import Logger
from twisted.internet import reactor
from kotori.util import slm
from kotori.errors import traceback_get_exception, last_error_and_traceback
from kotori.daq.intercom.wamp import WampApplication, WampSession
from kotori.daq.intercom.udp import UdpBusForwarder
from kotori.daq.storage.influx import BusInfluxForwarder
from kotori.daq.graphing.grafana import GrafanaManager
from kotori.vendor.lst.message import BinaryMessageAdapter
from kotori.vendor.lst.h2m.util import setup_h2m_structs

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
        logger.info('Starting UDPReceiver')
        # TODO: decouple hardcoded "setup_h2m_structs()"
        self.messenger = BinaryMessageAdapter(struct_registry=setup_h2m_structs())
        self.run()

    def run(self):
        """
        Run forwarding component, which actually moves data between UDP and the software bus
        """
        udp_port = int(self.config['lst-h2m']['udp_port'])
        topic = unicode(self.config['lst-h2m']['wamp_topic'])

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
        - ``_hex_``: raw message encoded in hex
        """
        data = self.messenger.to_dict(struct)
        data['_name_'] = struct._name_()
        data['_hex_'] = hexlify(struct._dump_())
        return data


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
        data = data.copy()
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
    Encapsulate receiving messages from software bus, mungling and storing into InfluxDB
    """

    def __init__(self, bus, config):
        self.bus = bus
        self.config = config
        logger.info('Starting InfluxStorage')
        topic = unicode(self.config['lst-h2m']['wamp_topic'])
        InfluxStorage(bus=self.bus, topic=topic, config=self.config)


class UdpSession(WampSession):
    component = UDPReceiver

class StorageSession(WampSession):
    component = StorageAdapter

def lst_boot(config, debug=False):
    wamp_uri = unicode(config.get('wamp', 'listen'))
    WampApplication(url=wamp_uri, realm=u'lst', session_class=UdpSession, config=config).make()
    WampApplication(url=wamp_uri, realm=u'lst', session_class=StorageSession, config=config).make()
