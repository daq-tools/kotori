# -*- coding: utf-8 -*-
# (c) 2014 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
# derived from https://github.com/tavendo/AutobahnPython/blob/master/examples/twisted/wamp/pubsub/simple/example2/server.py
import sys
from pkg_resources import resource_filename
from twisted.python import log
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.static import File
from autobahn.twisted import websocket
from autobahn.wamp import WampServerFactory, \
                          WampServerProtocol, exportRpc, WampClientFactory, WampClientProtocol

from urlparse import urlparse


client = None


class NodeRegistry(object):

    def __init__(self):
        self.nodes = {}
        self.sessions = {}

    def register(self, node_id):
        print "NodeRegistry.register:", node_id
        self.nodes[node_id] = True
        client.publish('http://ilaundry.useeds.de/dashboard#update', None)

    def unregister(self, node_id):
        print "NodeRegistry.unregister:", node_id
        try:
            del self.nodes[node_id]
        except KeyError:
            pass
        client.publish('http://ilaundry.useeds.de/dashboard#update', None)

    @exportRpc
    def get_nodelist(self):
        nodelist = self.nodes.keys()
        print "NodeRegistry.get_nodelist:", nodelist
        return nodelist

registry = NodeRegistry()


class MasterServerProtocol(WampServerProtocol):

    def onSessionOpen(self):
        self.registerForRpc(registry, "http://ilaundry.useeds.de/registry#")
        self.registerForPubSub("http://ilaundry.useeds.de/broadcast#", True)
        self.registerForPubSub("http://ilaundry.useeds.de/dashboard#", True)
        self.registerForPubSub("http://ilaundry.useeds.de/presence#", True)
        self.registerForPubSub("http://ilaundry.useeds.de/node/", True)



class MasterServerFactory(WampServerFactory):

    protocol = MasterServerProtocol

    def __init__(self, *args, **kwargs):
        WampServerFactory.__init__(self, *args, **kwargs)
        self.setProtocolOptions(allowHixie76 = True)

    def onClientSubscribed(self, proto, topic):
        print "client subscribed:  ", proto, topic
        uri = urlparse(topic)
        if uri.path == '/presence':
            node_id = uri.fragment
            registry.register(node_id)

    def onClientUnsubscribed(self, proto, topic):
        print "client unsubscribed:", proto, topic
        uri = urlparse(topic)
        if uri.path == '/presence':
            node_id = uri.fragment
            registry.unregister(node_id)


class MasterClientProtocol(WampClientProtocol):
    def onSessionOpen(self):
        global client
        client = self

class MasterClientFactory(WampClientFactory):
    protocol = MasterClientProtocol


def boot_master(websocket_uri, http_port, debug=False):

    print 'INFO: Starting master node'

    print 'INFO:   Starting WebSocket service on', websocket_uri
    factory = MasterServerFactory(websocket_uri, debugWamp = True)
    websocket.listenWS(factory)

    client_factory = MasterClientFactory(websocket_uri, debug=False, debugCodePaths=False, debugWamp=debug, debugApp=False)
    websocket.connectWS(client_factory)

    document_root = resource_filename('ilaundry.web', '')

    webdir = File(document_root)
    web = Site(webdir)

    print 'INFO:   Starting HTTP service on port', http_port
    reactor.listenTCP(http_port, web)


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
