# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
# https://pypi.python.org/pypi/twisted-mqtt
# https://github.com/astrorafael/twisted-mqtt/
from twisted.logger import Logger
from twisted.internet import reactor, task
from twisted.application.service import Service
from twisted.internet.endpoints import TCP4ClientEndpoint
from mqtt.client.factory import MQTTFactory

log = Logger()


class HiveeyesMqttAdapter(Service):

    def gotProtocol(self, p):
        self.protocol = p
        d = p.connect("kotori.mqtt", keepalive=0)
        d.addCallback(self.subscribe)
        #d.addCallback(self.prepareToPublish)

    def subscribe(self, *args):
        d = self.protocol.subscribe("foo/bar/baz", 0)
        e = self.protocol.subscribe("hiveeyes/#", 0)
        self.protocol.setPublishHandler(self.onPublish)

    def onPublish(self, topic, payload, qos, dup, retain, msgId):
        log.debug("topic={topic}, msg={payload} qos={qos}, dup={dup} retain={retain}, msgId={id}", topic=topic, payload=payload,
            qos=qos, dup=dup, retain=retain, id=msgId)

        if topic.startswith('hiveeyes'):
            # TODO: store to database
            pass

    def prepareToPublish(self, *args):
        self.task = task.LoopingCall(self.publish)
        self.task.start(5.0)

    def publish(self):
        d = self.protocol.publish(topic="foo/bar/baz", message="hello friends")
        d.addErrback(self.printError)

    def printError(self, *args):
        log.debug("args={args!s}", args=args)
        reactor.stop()


def he_boot_mqtt_adapter(broker_host, broker_port=1883, debug=False):

    print 'INFO: Starting MQTT adapter. broker=', broker_host, broker_port

    factory = MQTTFactory(profile=MQTTFactory.PUBLISHER | MQTTFactory.SUBSCRIBER)
    point   = TCP4ClientEndpoint(reactor, broker_host, broker_port)
    serv    = HiveeyesMqttAdapter()

    d = point.connect(factory).addCallback(serv.gotProtocol)
