# -*- coding: utf-8 -*-
# (c) 2014 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
# derived from https://github.com/tavendo/AutobahnPython/blob/master/examples/twisted/wamp/pubsub/simple/example2/client.py
import sys
from twisted.python import log
from twisted.internet import reactor
from autobahn.twisted.websocket import connectWS
from autobahn.wamp import WampClientFactory, WampClientProtocol

from util import tts_say

NODE_ID = '0xabcdef'
node_manager = None

class NodeProtocol(WampClientProtocol):
    """
    Implements various node services:
    - Heartbeat
    - Text-to-Speech
    """

    def heartbeat(self):
        self.publish("broadcast:node-heartbeat", NODE_ID)
        # FIXME: make this configurable as "heartbeat interval"
        reactor.callLater(15, self.heartbeat)

    def say(self, topic, message, language='de'):
        return tts_say(message, language=language)

    def onSessionOpen(self):
        print "Node service ready"
        self.prefix("broadcast", "http://ilaundry.useeds.de/broadcast#")
        self.prefix("node", "http://ilaundry.useeds.de/node/washer-1#")
        self.subscribe("broadcast:node-heartbeat", self.dump_event)
        self.subscribe("node:say", self.dump_event)
        self.subscribe("node:say", self.say)

        self.heartbeat()

    def connectionLost(self, reason):
        print "Node service defunct, reason:", reason
        #reactor.callLater(2, node_manager.connect)

    def dump_event(self, topic, event):
        print "dump_event:", topic, event


class NodeClientFactory(WampClientFactory):

    protocol = NodeProtocol

    def __init__(self, url, **kwargs):
        return WampClientFactory.__init__(self, url, **kwargs)

    def stopFactory(self):
        WampClientFactory.stopFactory(self)
        # FIXME: make this configurable as "reconnect interval"
        reactor.callLater(5, node_manager.connect)


class NodeManager(object):

    def __init__(self, debug=False):
        self.debug = debug

    def connect(self):
        factory = NodeClientFactory("ws://localhost:9000", debug=False, debugCodePaths=False, debugWamp=self.debug, debugApp=False)
        connectWS(factory)


def run():
    log.startLogging(sys.stdout)

    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        debug = True
    else:
        debug = False

    # startup greeting
    tts_say('Herzlich Willkommen')

    # connect to master service
    global node_manager
    node_manager = NodeManager(debug=debug)
    reactor.callLater(0, node_manager.connect)
    reactor.run()

if __name__ == '__main__':
    run()
