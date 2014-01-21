# -*- coding: utf-8 -*-
# (c) 2014 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
# derived from https://github.com/tavendo/AutobahnPython/blob/master/examples/twisted/wamp/pubsub/simple/example2/server.py
import sys
from twisted.python import log
from twisted.internet import reactor
from autobahn.twisted import websocket
from autobahn.wamp import WampServerFactory, \
                          WampServerProtocol, exportRpc, WampClientFactory, WampClientProtocol

from urlparse import urlparse, parse_qs


client = None


class NodeRegistry(object):

    def __init__(self):
        self.nodes = {}
        self.sessions = {}

    def register(self, node_id, hostname=None):
        print "NodeRegistry.register:", node_id
        self.nodes[node_id] = {'hostname': hostname}
        client.publish('http://ilaundry.useeds.de/dashboard#update', None)

    def unregister(self, node_id):
        print "NodeRegistry.unregister:", node_id
        try:
            del self.nodes[node_id]
        except KeyError:
            pass
        client.publish('http://ilaundry.useeds.de/dashboard#update', None)

    @exportRpc
    def get_nodes(self):
        print "NodeRegistry.get_nodes:", self.nodes
        return self.nodes

registry = NodeRegistry()


class MasterServerProtocol(WampServerProtocol):

    def onSessionOpen(self):
        self.registerForRpc(registry, "http://ilaundry.useeds.de/registry#")
        self.registerForPubSub("http://ilaundry.useeds.de/broadcast#", True)
        self.registerForPubSub("http://ilaundry.useeds.de/dashboard#", True)
        self.registerForPubSub("http://ilaundry.useeds.de/presence", True)
        self.registerForPubSub("http://ilaundry.useeds.de/node/", True)



class MasterServerFactory(WampServerFactory):

    protocol = MasterServerProtocol

    def __init__(self, *args, **kwargs):
        WampServerFactory.__init__(self, *args, **kwargs)
        self.setProtocolOptions(allowHixie76 = True)

    def onClientSubscribed(self, proto, topic):
        print "subscribed:  ", proto, topic
        uri = urlparse(topic)
        if uri.path == '/presence':
            params = parse_qs(uri.query)
            node_id = params['node_id'][0]
            hostname = params['hostname'][0]
            registry.register(node_id, hostname)

    def onClientUnsubscribed(self, proto, topic):
        print "unsubscribed:", proto, topic
        uri = urlparse(topic)
        if uri.path == '/presence':
            params = parse_qs(uri.query)
            node_id = params['node_id'][0]
            registry.unregister(node_id)


class MasterClientProtocol(WampClientProtocol):
    def onSessionOpen(self):
        global client
        client = self

class MasterClientFactory(WampClientFactory):
    protocol = MasterClientProtocol


def boot_master(websocket_uri, debug=False):

    print 'INFO: Starting WebSocket master service on', websocket_uri
    factory = MasterServerFactory(websocket_uri, debugWamp = True)
    websocket.listenWS(factory)

    client_factory = MasterClientFactory(websocket_uri, debug=False, debugCodePaths=False, debugWamp=debug, debugApp=False)
    websocket.connectWS(client_factory)



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
