# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
from twisted.logger import Logger
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from twisted.internet.protocol import DatagramProtocol
from autobahn.twisted.wamp import ApplicationSession
from kotori.bus.wamp import WampBus
from kotori.vendor.hydro2motion.util.geo import turn_xyz_into_llh

log = Logger()

app_session = None


class UdpPublisher(ApplicationSession):
    """
    Simple message publishing with Autobahn WebSockets.

    derived from:
    - https://github.com/tavendo/AutobahnPython/blob/master/examples/twisted/wamp/basic/pubsub/basic/frontend.py
    - https://github.com/tavendo/AutobahnPython/blob/master/examples/twisted/wamp/pubsub/simple/example2/client.py
    - https://github.com/tavendo/AutobahnPython/blob/master/examples/twisted/wamp/session/fromoutside/client.py
    """

    def onJoin(self, details):
        log.info("UdpPublisher joined WAMP bus")

        global app_session
        app_session = self

    def onDisconnect(self):
        log.info("UdpPublisher disconnected from WAMP bus")


class UdpAdapter(DatagramProtocol):
    # https://twistedmatrix.com/documents/15.0.0/core/howto/udp.html

    @inlineCallbacks
    def datagramReceived(self, data, addr):
        (host, port) = addr
        log.info("Received via UDP from %s:%d: %r " % (host, port, data))

        try:
            payload = data.split(';')
            GPS_X           = int(float(payload[24]))
            GPS_Y           = int(float(payload[25]))
            GPS_Z           = int(float(payload[26]))

            x = GPS_X / 100.0
            y = GPS_Y / 100.0
            z = GPS_Z / 100.0


            llh = turn_xyz_into_llh(x, y, z, "wgs84")
            lat = llh[0]
            lng = llh[1]

            seq = (data, str(lat), str(lng))

            jdata = ";".join(seq)

        except ValueError:
            log.warn('Could not decode data: {}'.format(data))

        # ECHO
        #self.transport.write(data, (host, port))

        # forward
        yield app_session.publish(u'de.elmyra.kotori.telemetry.data', jdata)


def listen_udp(udp_port):
    log.info('Starting udp adapter on port "{}"'.format(udp_port))
    reactor.listenUDP(udp_port, UdpAdapter())


def h2m_boot_udp_adapter(settings, debug=False):

    websocket_uri = str(settings.wamp.uri)
    udp_port = int(settings.hydro2motion.udp_port)

    wamp_bus = WampBus(uri=websocket_uri, session_factory=UdpPublisher)
    wamp_bus.connect()
    listen_udp(udp_port)
