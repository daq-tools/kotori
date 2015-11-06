# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
from twisted.logger import Logger
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from twisted.internet.protocol import DatagramProtocol
from autobahn.twisted.wamp import ApplicationRunner, ApplicationSession
from kotori.vendor.hydro2motion.util.geo import turn_xyz_into_llh

logger = Logger()


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
        print("session attached")

        global app_session
        app_session = self


    def onDisconnect(self):
        print("disconnected")
        #reactor.stop()



class UdpAdapter(DatagramProtocol):
    # https://twistedmatrix.com/documents/15.0.0/core/howto/udp.html

    @inlineCallbacks
    def datagramReceived(self, data, (host, port)):
        logger.info("Received via UDP from %s:%d: %r " % (host, port, data))

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
            logger.warn('Could not decode data: {}'.format(data))

        # ECHO
        #self.transport.write(data, (host, port))

        # forward
        yield app_session.publish(u'de.elmyra.kotori.telemetry.data', jdata)


def connect_wamp(wsuri):

    # connect to crossbar router/broker
    runner = ApplicationRunner(wsuri, u'kotori-realm')
    #runner = ApplicationRunner("ws://master.example.com:9000/ws", "kotori-realm")

    d = runner.run(UdpPublisher, start_reactor=False)

    def croak(ex, *args):
        logger.error('Problem in UdpAdapter, please also check if "crossbar" WAMP broker is running at {wsuri}'.format(wsuri=wsuri))
        logger.error("{ex}, args={args!s}", ex=ex.getTraceback(), args=args)
        reactor.stop()
        raise ex
    d.addErrback(croak)


def listen_udp(udp_port):
    print 'INFO: Starting udp adapter on port', udp_port
    reactor.listenUDP(udp_port, UdpAdapter())


def h2m_boot_udp_adapter(config, debug=False):

    websocket_uri = unicode(config.get('wamp', 'listen'))
    udp_port = int(config.get('hydro2motion', 'udp_port'))

    connect_wamp(websocket_uri)
    listen_udp(udp_port)

