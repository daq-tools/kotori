# -*- coding: utf-8 -*-
# (c) 2014-2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import socket
import sys
from autobahn.twisted.wamp import ApplicationRunner, ApplicationSession
from twisted.internet.defer import inlineCallbacks
from twisted.python import log
from twisted.internet import reactor

class KotoriClient(ApplicationSession):
    """
    Simple message publishing with Autobahn WebSockets.

    derived from:
    - https://github.com/tavendo/AutobahnPython/blob/master/examples/twisted/wamp/basic/pubsub/basic/frontend.py
    - https://github.com/tavendo/AutobahnPython/blob/master/examples/twisted/wamp/pubsub/simple/example2/client.py
    """

    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")

        yield self.publish("de.elmyra.kotori.broadcast.node-activity", {'node_id': 'Hello!', 'state': True}, excludeMe=False)
        yield self.publish("de.elmyra.kotori.broadcast.operator-presence", True, excludeMe=False)
        #yield self.publish("de.elmyra.kotori.broadcast.operator-presence", False, excludeMe=False)

        # send telemetry data
        yield self.publish("de.elmyra.kotori.telemetry.data", 'WAMP hello', excludeMe=False)
        yield self.publish("de.elmyra.kotori.telemetry.data", {'attribute1': 'value1', 'attribute2': 'value2'}, excludeMe=False)

        reactor.callLater(0.1, reactor.stop)

    def onDisconnect(self):
        print("disconnected")
        reactor.stop()

def run_wamp_client():
    log.startLogging(sys.stdout)
    runner = ApplicationRunner("ws://localhost:9000/ws", "kotori-realm")
    #runner = ApplicationRunner("ws://master.example.com:9000/ws", "kotori-realm")
    runner.run(KotoriClient, start_reactor=False)
    reactor.run()


# derived from https://twistedmatrix.com/documents/15.0.0/core/howto/udp.html
def run_udp_client():
    log.startLogging(sys.stdout)

    data = 'UDP hello'

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.sendto(data, ('127.0.0.1', 7777))

if __name__ == '__main__':
    #run_wamp_client()
    run_udp_client()
