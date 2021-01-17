# -*- coding: utf-8 -*-
# (c) 2014-2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
#
# derived from https://github.com/tavendo/AutobahnPython/blob/master/examples/twisted/wamp/pubsub/simple/example2/client.py
import sys
from autobahn.twisted.wamp import ApplicationRunner, ApplicationSession
from twisted.internet.defer import inlineCallbacks
from twisted.python import log
from twisted.internet import reactor
from autobahn.twisted.websocket import connectWS, WampWebSocketClientProtocol, WampWebSocketClientFactory
from kotori.util.common import NodeId, get_hostname
from kotori.vendor.ilaundry.node.util import tts_say

node_manager = None
NODE_ID = str(NodeId())
NODE_HOSTNAME = get_hostname()


class NodeProtocol(WampWebSocketClientProtocol):
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

        self.prefix("broadcast", "de.elmyra.kotori.broadcast")
        self.prefix("presence", "http://kotori.elmyra.de/presence?")
        self.prefix("node", "http://kotori.elmyra.de/node/{0}#".format(NODE_ID))

        self.subscribe("broadcast:node-heartbeat", self.dump_event)

        self.subscribe("presence:node_id={0}&hostname={1}".format(NODE_ID, NODE_HOSTNAME), lambda: x)

        self.subscribe("node:say", self.dump_event)
        self.subscribe("node:say", self.say)

        print("INFO:   -> Node successfully connected to master")

        self.heartbeat()

        reactor.callLater(0, node_manager.start_features, self)


    def connectionLost(self, reason):
        print("ERROR: Connection lost, reason:", reason)
        #reactor.callLater(2, node_manager.connect)

    def dump_event(self, topic, event):
        print("dump_event:", topic, event)


class NodeClientFactory(WampWebSocketClientFactory):

    protocol = NodeProtocol
    noisy = False

    def __init__(self, url, **kwargs):
        return WampWebSocketClientFactory.__init__(self, url, **kwargs)

    def clientConnectionFailed(self, connector, reason):
        print('NodeClientFactory.clientConnectionFailed:', reason)

    def clientConnectionLost(self, connector, reason):
        print('NodeClientFactory.clientConnectionLost:', reason)

    def stopFactory(self):
        print('NodeClientFactory.stopFactory')
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

        from kotori.vendor.ilaundry.node.feature import FeatureSet
        features = FeatureSet(NODE_ID, protocol)

        #actor = GpioOutput('P8_13')
        #actor.blink(0.2)


class KotoriNode(ApplicationSession):

    """
    An application component using the time service
    during 3 subsequent WAMP sessions, while the
    underlying transport continues to exist.
    """

    def __init__(self, config):
        ApplicationSession.__init__(self, config)
        self.count = 0

    @inlineCallbacks
    def onJoin(self, details):
        print("Realm joined (WAMP session started).")

        #self.heartbeat_loop()

        self.subscribe(self.heartbeat, u'de.elmyra.kotori.broadcast.heartbeat')
        self.subscribe(self.dump_event, u'de.elmyra.kotori.broadcast.operator-presence')

        try:
            now = yield self.call('com.timeservice.now')
        except Exception as e:
            print(("Error: {}".format(e)))
        else:
            print(("Current time from time service: {}".format(now)))


        yield self.publish(u'de.elmyra.kotori.telemetry.data', 'hello world')

        #self.leave()

    def onLeave(self, details):
        print("Realm left (WAMP session ended).")
        self.count += 1
        if self.count < 3:
            self.join("kotori-realm")
        else:
            self.disconnect()
        ApplicationSession.onLeave(self, details)

    def onDisconnect(self):
        print("Transport disconnected.")
        #reactor.stop()

    def heartbeat_loop(self, *args, **kwargs):
        self.heartbeat(*args, **kwargs)
        # FIXME: make this configurable as "heartbeat interval"
        reactor.callLater(30, self.heartbeat_loop)

    def heartbeat(self, *args, **kwargs):
        print("KotoriNode.heartbeat publish")
        self.publish(u'de.elmyra.kotori.broadcast.heartbeat', NODE_ID)


    def dump_event(self, *args, **kwargs):
        print("dump_event:", {'args': args, 'kwargs': kwargs})
        #print self, dir(self)


def boot_node(websocket_uri, debug=False, trace=False):

    print('INFO: Starting node service, connecting to', websocket_uri)

    # connect to master service
    """
    global node_manager
    node_manager = NodeManager(websocket_uri, debug=debug)
    reactor.callLater(0, node_manager.master_connect)
    """

    runner = ApplicationRunner(websocket_uri, u'kotori-realm', debug=trace, debug_wamp=debug, debug_app=debug)
    runner.run(KotoriNode, start_reactor=False)

    #app = Application()
    #app.run(url=websocket_uri, realm='kotori-realm', debug=True, debug_wamp=True, debug_app=True, start_reactor=False)


def run():
    log.startLogging(sys.stdout)

    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        debug = True
    else:
        debug = False

    # startup greeting
    #tts_say('Herzlich Willkommen')

    WEBSOCKET_URI = 'ws://localhost:9000'
    #WEBSOCKET_URI = 'ws://master.example.com:9000'
    boot_node(WEBSOCKET_URI, debug)

    reactor.run()


if __name__ == '__main__':
    run()
