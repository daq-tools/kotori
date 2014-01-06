# -*- coding: utf-8 -*-
# (c) 2014 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
# derived from https://github.com/tavendo/AutobahnPython/blob/master/examples/twisted/wamp/pubsub/simple/example2/client.py
import os
import sys
import shelve
from appdirs import user_data_dir
from uuid import uuid4
from twisted.python import log
from twisted.internet import reactor
from autobahn.twisted.websocket import connectWS
from autobahn.wamp import WampClientFactory, WampClientProtocol

from util import tts_say

NODE_ID = 'NODE_UNKNOWN'
#WEBSOCKET_URI = 'ws://localhost:9000'
WEBSOCKET_URI = 'ws://master.ilaundry.useeds.elmyra.de:9000'
node_manager = None

class ConfigStore(dict):

    def __init__(self):
        self.app_data_dir = user_data_dir('iLaundry', 'useeds')
        if not os.path.exists(self.app_data_dir):
            os.makedirs(self.app_data_dir)
        self.config_file = os.path.join(self.app_data_dir, 'config')
        self.store = shelve.open(self.config_file, writeback=True)

    def has_key(self, key):
        return self.store.has_key(key)

    def __getitem__(self, key):
        return self.store[key]

    def __setitem__(self, key, value):
        self.store[key] = value
        self.store.sync()

config = ConfigStore()
if not config.has_key('uuid'):
    config['uuid'] = str(uuid4())
NODE_ID = config['uuid']
print "NODE ID:", NODE_ID


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

        self.prefix("broadcast", "http://ilaundry.useeds.de/broadcast#")
        self.prefix("presence", "http://ilaundry.useeds.de/presence#")
        self.prefix("node", "http://ilaundry.useeds.de/node/{}#".format(NODE_ID))

        self.subscribe("broadcast:node-heartbeat", self.dump_event)

        self.subscribe("presence:{0}".format(NODE_ID), lambda: x)

        self.subscribe("node:say", self.dump_event)
        self.subscribe("node:say", self.say)

        print "Node service ready"

        #self.heartbeat()

    def connectionLost(self, reason):
        print "Node service defunct, reason:", reason
        #reactor.callLater(2, node_manager.connect)

    def dump_event(self, topic, event):
        print "dump_event:", topic, event


class NodeClientFactory(WampClientFactory):

    protocol = NodeProtocol
    noisy = False

    def __init__(self, url, **kwargs):
        return WampClientFactory.__init__(self, url, **kwargs)

    def stopFactory(self):
        WampClientFactory.stopFactory(self)
        # FIXME: make this configurable as "reconnect interval"
        reactor.callLater(2, node_manager.connect)


class NodeManager(object):

    def __init__(self, websocket_uri, debug=False):
        self.websocket_uri = websocket_uri
        self.debug = debug

    def connect(self):
        factory = NodeClientFactory(self.websocket_uri, debug=False, debugCodePaths=False, debugWamp=self.debug, debugApp=False)
        connectWS(factory)


def run():
    log.startLogging(sys.stdout)

    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        debug = True
    else:
        debug = False

    # startup greeting
    #tts_say('Herzlich Willkommen')

    # connect to master service
    global node_manager
    node_manager = NodeManager(WEBSOCKET_URI, debug=debug)
    reactor.callLater(0, node_manager.connect)
    reactor.run()

if __name__ == '__main__':
    run()
