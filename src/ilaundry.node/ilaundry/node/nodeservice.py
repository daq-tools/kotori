# -*- coding: utf-8 -*-
# (c) 2014 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
# derived from https://github.com/tavendo/AutobahnPython/blob/master/examples/twisted/wamp/pubsub/simple/example2/client.py
import sys
from twisted.python import log
from twisted.internet import reactor
from autobahn.twisted.websocket import connectWS
from autobahn.wamp import WampClientFactory, WampClientProtocol
from ilaundry.util import NodeId, get_hostname
from util import tts_say

node_manager = None
NODE_ID = str(NodeId())
NODE_HOSTNAME = get_hostname()

class NodeProtocol(WampClientProtocol):
    """
    Implements various node services:
    - Heartbeat
    - Text-to-Speech
    """

    def heartbeat(self):
        self.publish("broadcast:node-heartbeat", NODE_ID)
        # FIXME: make this configurable as "heartbeat interval"
        reactor.callLater(60, self.heartbeat)

    def say(self, topic, message, language='de'):
        return tts_say(message, language=language)

    def onSessionOpen(self):

        self.prefix("broadcast", "http://ilaundry.useeds.de/broadcast#")
        self.prefix("presence", "http://ilaundry.useeds.de/presence?")
        self.prefix("node", "http://ilaundry.useeds.de/node/{0}#".format(NODE_ID))

        self.subscribe("broadcast:node-heartbeat", self.dump_event)

        self.subscribe("presence:node_id={0}&hostname={1}".format(NODE_ID, NODE_HOSTNAME), lambda: x)

        self.subscribe("node:say", self.dump_event)
        self.subscribe("node:say", self.say)

        print "INFO:   -> Node successfully connected to master"

        self.heartbeat()

        reactor.callLater(0, node_manager.start_features, self)


    def connectionLost(self, reason):
        print "ERROR: Connection lost, reason:", reason
        #reactor.callLater(2, node_manager.connect)

    def dump_event(self, topic, event):
        print "dump_event:", topic, event


class NodeClientFactory(WampClientFactory):

    protocol = NodeProtocol
    noisy = False

    def __init__(self, url, **kwargs):
        return WampClientFactory.__init__(self, url, **kwargs)

    def clientConnectionFailed(self, connector, reason):
        print 'NodeClientFactory.clientConnectionFailed:', reason

    def clientConnectionLost(self, connector, reason):
        print 'NodeClientFactory.clientConnectionLost:', reason

    def stopFactory(self):
        print 'NodeClientFactory.stopFactory'
        WampClientFactory.stopFactory(self)
        # FIXME: make this configurable as "reconnect interval"
        reactor.callLater(2, node_manager.master_connect)


class NodeManager(object):

    def __init__(self, websocket_uri, debug=False):
        self.websocket_uri = websocket_uri
        self.debug = debug

    def master_connect(self):
        factory = NodeClientFactory(self.websocket_uri, debug=False, debugCodePaths=False, debugWamp=self.debug, debugApp=False)
        connectWS(factory)

    def start_features(self, protocol):

        from feature import FeatureSet
        features = FeatureSet(NODE_ID, protocol)

        #actor = GpioOutput('P8_13')
        #actor.blink(0.2)


def boot_node(websocket_uri, debug=False):

    print 'INFO: Starting node service, connecting to', websocket_uri

    # connect to master service
    global node_manager
    node_manager = NodeManager(websocket_uri, debug=debug)
    reactor.callLater(0, node_manager.master_connect)


def run():
    log.startLogging(sys.stdout)

    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        debug = True
    else:
        debug = False

    # startup greeting
    #tts_say('Herzlich Willkommen')

    #WEBSOCKET_URI = 'ws://localhost:9000'
    WEBSOCKET_URI = 'ws://master.ilaundry.useeds.elmyra.de:9000'
    boot_node(WEBSOCKET_URI, debug)

    reactor.run()

if __name__ == '__main__':
    run()
