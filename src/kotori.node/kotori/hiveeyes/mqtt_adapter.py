# -*- coding: utf-8 -*-
# https://pypi.python.org/pypi/twisted-mqtt
# https://github.com/astrorafael/twisted-mqtt/
from twisted.logger import Logger, LogLevel
from twisted.internet import reactor, task
from twisted.application.service import Service
from twisted.internet.endpoints import TCP4ClientEndpoint

from mqtt.client.factory import MQTTFactory
from mqtt.logger import startLogging

log = Logger()


class MyService(Service):

    def gotProtocol(self, p):
        self.protocol = p
        d = p.connect("TwistedMQTT-pubsubs", keepalive=0)
        d.addCallback(self.subscribe)
        d.addCallback(self.prepareToPublish)

    def subscribe(self, *args):
        d = self.protocol.subscribe("foo/bar/baz", 0 )
        self.protocol.setPublishHandler(self.onPublish)

    def onPublish(self, topic, payload, qos, dup, retain, msgId):
        log.debug("topic = {topic}, msg={payload} qos = {qos}, dup ={dup} retain={retain}, msgId={id}", topic=topic, payload=payload,
            qos=qos, dup=dup, retain=retain, id=msgId)

    def prepareToPublish(self, *args):
        self.task = task.LoopingCall(self.publish)
        self.task.start(5.0)

    def publish(self):
        d = self.protocol.publish(topic="foo/bar/baz", message="hello friends")
        d.addErrback(self.printError)

    def printError(self, *args):
        log.debug("args={args!s}", args=args)
        reactor.stop()


if __name__ == '__main__':
    import sys
    log = Logger()
    startLogging(sys.stdout, LogLevel.debug)

    factory = MQTTFactory(profile=MQTTFactory.PUBLISHER | MQTTFactory.SUBSCRIBER)
    point   = TCP4ClientEndpoint(reactor, "test.mosquitto.org", 1883)
    serv    = MyService()

    d = point.connect(factory).addCallback(serv.gotProtocol)
    reactor.run()
