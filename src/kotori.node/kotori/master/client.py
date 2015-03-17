# -*- coding: utf-8 -*-
# (c) 2014 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
# derived from https://github.com/tavendo/AutobahnPython/blob/master/examples/twisted/wamp/pubsub/simple/example2/client.py
import sys
from twisted.python import log
from twisted.internet import reactor
from autobahn.twisted.websocket import connectWS
from autobahn.wamp import WampClientFactory, WampClientProtocol


class MyClientProtocol(WampClientProtocol):
    """
    Demonstrates simple Publish & Subscribe (PubSub) with Autobahn WebSockets.
    """

    def printEvent(self, topicUri, event):
        print "printEvent", topicUri, event

    def sendSimpleEvent(self):
        self.publish("http://example.com/simple", "Hello!")
        #      self.publish("http://example.com/simple", "Hello!", excludeMe = False, eligible = [self.session_id])
        reactor.callLater(2, self.sendSimpleEvent)

    def onEvent1(self, topicUri, event):
        print "onEvent1"
        self.counter += 1
        self.publish("event:myevent2", {"trigger": event, "counter": self.counter}, excludeMe=False)

    def onSessionOpen(self):
        print "onSessionOpen"

        """
        self.counter = 0
        self.subscribe("http://example.com/simple", self.printEvent)
        self.sendSimpleEvent()

        self.prefix("event", "http://example.com/event#")

        self.subscribe("event:myevent1", self.onEvent1)
        self.subscribe("event:myevent2", self.printEvent)

        self.publish("event:myevent1", "Hello!", excludeMe=False)
        """


        self.prefix("broadcast", "http://kotori.elmyra.de/broadcast#")
        self.publish("broadcast:node-activity", {'node_id': 'Hello!', 'state': True}, excludeMe=False)
        self.publish("broadcast:operator-presence", True, excludeMe=False)
        #self.publish("broadcast:operator-presence", False, excludeMe=False)
        reactor.callLater(1, reactor.stop)


if __name__ == '__main__':

    log.startLogging(sys.stdout)
    factory = WampClientFactory("ws://localhost:9000")
    #factory = WampClientFactory("ws://master.example.com:9000")
    factory.protocol = MyClientProtocol
    connectWS(factory)
    reactor.run()
