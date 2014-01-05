# -*- coding: utf-8 -*-
# (c) 2014 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
# derived from https://github.com/tavendo/AutobahnPython/blob/master/examples/twisted/wamp/pubsub/simple/example2/server.py
import sys
from pkg_resources import resource_filename

from twisted.python import log
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.static import File

from autobahn.twisted.websocket import listenWS
from autobahn.wamp import WampServerFactory, \
                          WampServerProtocol


class MyServerProtocol(WampServerProtocol):

    def onSessionOpen(self):
        self.registerForPubSub("http://ilaundry.useeds.de/broadcast#", True)
        self.registerForPubSub("http://ilaundry.useeds.de/node/", True)


def run():

    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        log.startLogging(sys.stdout)
        debug = True
    else:
        debug = False

    websocket_uri = 'ws://localhost:9000'
    http_port = 35000

    print 'Starting WebSocket service on', websocket_uri
    factory = WampServerFactory(websocket_uri, debugWamp = True)
    factory.protocol = MyServerProtocol
    factory.setProtocolOptions(allowHixie76 = True)
    listenWS(factory)

    document_root = resource_filename('ilaundry.web', '')

    webdir = File(document_root)
    web = Site(webdir)

    print 'Starting HTTP service on port', http_port
    reactor.listenTCP(http_port, web)

    reactor.run()


if __name__ == '__main__':
    run()
