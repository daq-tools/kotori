# -*- coding: utf-8 -*-
# (c) 2014-2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
#
# derived from https://github.com/tavendo/AutobahnPython/blob/master/examples/twisted/wamp/pubsub/simple/example2/server.py
import sys
import datetime
from copy import deepcopy
from urllib.parse import urlparse, parse_qs

from autobahn.twisted.wamp import ApplicationRunner, ApplicationSession
from autobahn.twisted.websocket import WampWebSocketClientProtocol, WampWebSocketClientFactory
from autobahn.twisted.websocket import WampWebSocketServerProtocol, WampWebSocketServerFactory
from twisted.python import log
from twisted.internet import reactor
from kotori.util.common import ConfigStoreJson


client = None


class NodeRegistry(object):

    def __init__(self):
        self.nodes = {}
        self.sessions = {}
        self.config = ConfigStoreJson()
        #print '----------------------', self.config.store
        #print '----------------------', self.config.get('nodes')
        #self.nodes = self.config.get('nodes', {})
        #print '======================', self.nodes

    def persist(self):
        print("============= persist", self.nodes)
        #self.config['nodes'].update(self.nodes)
        #del self.config['nodes']
        self.config['nodes'] = {'haha': {'hehe': 'dscsdcsdcsdcc'}}
        #self.config['nodes'] = self.nodes.copy()
        self.config['nodes2'] = deepcopy(self.nodes)
        self.config['ttt'] = 'huhu'

        #   self.config['nodes']['abc'] = 'def2'
        #self.nodes.setdefault('ghi', {})['kli'] = 'DEFUNCT'
        #self.config['ghi']['jkl'] = 'defunct'

    def register(self, node_id, hostname=None):
        print("NodeRegistry.register:", node_id)
        self.nodes[node_id] = {'hostname': hostname}
        self.persist()
        client.publish('http://kotori.elmyra.de/dashboard#update', None)

    def unregister(self, node_id):
        print("NodeRegistry.unregister:", node_id)
        try:
            del self.nodes[node_id]
            self.persist()
        except KeyError:
            pass
        client.publish('http://kotori.elmyra.de/dashboard#update', None)

    #@exportRpc
    def get_nodes(self):
        print("NodeRegistry.get_nodes:", self.nodes)
        return self.nodes

    #@exportRpc
    def set_node_label(self, node_id, label):
        print("NodeRegistry.set_node_label:", node_id, label)
        self.nodes.setdefault(node_id, {})['label'] = label
        print(self.nodes[node_id])
        self.persist()

#registry = NodeRegistry()


class MasterServerProtocol(WampWebSocketServerProtocol):

    def onSessionOpen(self):
        self.registerForRpc(registry, "http://kotori.elmyra.de/registry#")
        self.registerForPubSub("http://kotori.elmyra.de/broadcast#", True)
        self.registerForPubSub("http://kotori.elmyra.de/dashboard#", True)
        self.registerForPubSub("http://kotori.elmyra.de/presence", True)
        self.registerForPubSub("http://kotori.elmyra.de/node/", True)



class MasterServerFactory(WampWebSocketServerFactory):

    protocol = MasterServerProtocol

    def __init__(self, *args, **kwargs):
        WampServerFactory.__init__(self, *args, **kwargs)
        self.setProtocolOptions(allowHixie76 = True)

    def onClientSubscribed(self, proto, topic):
        print("subscribed:  ", proto, topic)
        uri = urlparse(topic)
        if uri.path == '/presence':
            params = parse_qs(uri.query)
            node_id = params['node_id'][0]
            hostname = params['hostname'][0]
            registry.register(node_id, hostname)

    def onClientUnsubscribed(self, proto, topic):
        print("unsubscribed:", proto, topic)
        uri = urlparse(topic)
        if uri.path == '/presence':
            params = parse_qs(uri.query)
            node_id = params['node_id'][0]
            registry.unregister(node_id)


class MasterClientProtocol(WampWebSocketClientProtocol):
    def onSessionOpen(self):
        global client
        client = self

class MasterClientFactory(WampWebSocketClientFactory):
    protocol = MasterClientProtocol


class Component(ApplicationSession):

    """
    A simple time service application component.
    """

    def onJoin(self, details):

        def utcnow():
            now = datetime.datetime.utcnow()
            return now.strftime("%Y-%m-%dT%H:%M:%SZ")

        self.register(utcnow, 'com.timeservice.now')


def boot_master(websocket_uri, debug=False, trace=False):

    print('INFO: Starting WebSocket master service on', websocket_uri)
    """
    factory = MasterServerFactory(websocket_uri, debugWamp = True)
    websocket.listenWS(factory)

    client_factory = MasterClientFactory(websocket_uri, debug=False, debugCodePaths=False, debugWamp=debug, debugApp=False)
    websocket.connectWS(client_factory)
    """

    runner = ApplicationRunner(websocket_uri, u'kotori-realm', debug=trace, debug_wamp=debug, debug_app=debug)
    runner.run(Component, start_reactor=False)


def run():

    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        log.startLogging(sys.stdout)
        debug = True
    else:
        debug = False

    websocket_uri = 'ws://localhost:9000'
    http_port = 35000

    boot_master(websocket_uri, http_port, debug)

    reactor.run()


if __name__ == '__main__':
    run()
