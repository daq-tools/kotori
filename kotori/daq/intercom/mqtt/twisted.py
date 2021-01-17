# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl <andreas.motl@getkotori.org>
# https://pypi.python.org/pypi/twisted-mqtt
# https://github.com/astrorafael/twisted-mqtt/
from __future__ import absolute_import
from twisted.logger import Logger
from twisted.internet import reactor
from twisted.application.service import Service
from twisted.internet.endpoints import TCP4ClientEndpoint
from kotori.daq.intercom.mqtt.base import BaseMqttAdapter
from mqtt.client.factory import MQTTFactory

log = Logger()


class TwistedMqttAdapter(BaseMqttAdapter, Service):

    def connect(self):
        log.info('Connecting')
        factory = MQTTFactory(profile=MQTTFactory.PUBLISHER | MQTTFactory.SUBSCRIBER)
        point   = TCP4ClientEndpoint(reactor, self.broker_host, self.broker_port)
        d = point.connect(factory).addCallback(self.gotProtocol)
        d.addErrback(self.on_error)

    def gotProtocol(self, p):
        log.info('gotProtocol, connecting {name}', name=self.name)
        self.protocol = p
        #def later():
        d = p.connect(self.name, keepalive=0, cleanStart=True)
        d.addCallback(self.subscribe)
        #d.addCallback(self.prepareToPublish)
        #reactor.callLater(random.randint(2, 7), later)
        #reactor.callInThread(later)

    def subscribe(self, *args):
        #d = self.protocol.subscribe("foo/bar/baz", 0)
        log.info(u"Subscribing to topics {subscriptions}. protocol={protocol}", subscriptions=self.subscriptions, protocol=self.protocol)
        for topic in self.subscriptions:
            log.info(u"Subscribing to topic '{topic}'", topic=topic)
            # Topic name **must not** be unicode, so casting to string
            e = self.protocol.subscribe(str(topic), 0)

        log.info(u"Setting callback handler: {callback}", callback=self.callback)
        self.protocol.setPublishHandler(self.on_message_twisted)
        """
        def cb(*args, **kwargs):
            log.info('publishHandler got called: name={name}, args={args}, kwargs={kwargs}', name=self.name, args=args, kwargs=kwargs)
            return reactor.callFromThread(self.callback, *args, **kwargs)
        self.protocol.setPublishHandler(cb)
        """

    def on_message_twisted(self, topic, payload, *args):
        # former def on_message(self, topic, payload, qos, dup, retain, msgId):
        kwargs = dict(zip(['qos', 'dup', 'retain', 'msgId'], args))
        log.debug('on_message: name={name}, topic={topic}, payload={payload}, kwargs={kwargs}', name=self.name, topic=topic, payload=payload, kwargs=kwargs)
        return self.callback(topic=topic, payload=payload, **kwargs)
