# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
#
# https://twistedmatrix.com/documents/15.0.0/core/howto/udp.html
from autobahn.twisted.wamp import ApplicationRunner, ApplicationSession, ApplicationSessionFactory
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from twisted.internet.protocol import DatagramProtocol

app_session = None

class UdpPublisher(ApplicationSession):
    """
    Simple message publishing with Autobahn WebSockets.

    derived from:
    - https://github.com/tavendo/AutobahnPython/blob/master/examples/twisted/wamp/basic/pubsub/basic/frontend.py
    - https://github.com/tavendo/AutobahnPython/blob/master/examples/twisted/wamp/pubsub/simple/example2/client.py
    - https://github.com/tavendo/AutobahnPython/blob/master/examples/twisted/wamp/session/fromoutside/client.py
    """

    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")

        global app_session
        app_session = self


    def onDisconnect(self):
        print("disconnected")
        reactor.stop()


def run_wamp_client():
    #log.startLogging(sys.stdout)
    runner = ApplicationRunner("ws://localhost:9000/ws", "kotori-realm")
    #runner = ApplicationRunner("ws://master.example.com:9000/ws", "kotori-realm")
    runner.run(UdpPublisher, start_reactor=False)



class UdpAdapter(DatagramProtocol):

    def datagramReceived(self, data, (host, port)):
        print "received %r from %s:%d" % (data, host, port)

        # ECHO
        #self.transport.write(data, (host, port))

        # forward
        app_session.publish(u'de.elmyra.kotori.telemetry.data', data)



def boot_udp_adapter(udp_port, debug=False):

    run_wamp_client()

    print 'INFO: Starting udp adapter on port', udp_port
    reactor.listenUDP(udp_port, UdpAdapter())
