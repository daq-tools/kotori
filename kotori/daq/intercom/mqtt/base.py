# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
# https://pypi.python.org/pypi/twisted-mqtt
# https://github.com/astrorafael/twisted-mqtt/
from __future__ import absolute_import
from twisted.logger import Logger

log = Logger()

class BaseMqttAdapter(object):

    def __init__(self, name, broker_host=u'localhost', broker_port=1883, debug=False, callback=None, subscriptions=None):
        self.name = name
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.callback = callback or self.on_message
        self.subscriptions = subscriptions or []

    def startService(self):
        log.info('Starting {class_name} {name}@{repr}. broker={broker_host}',
            class_name=self.__class__.__name__, name=self.name, repr=repr(self),
            broker_host=self.broker_host, broker_port=self.broker_port)
        self.running = 1
        self.connect()
        #reactor.callInThread(self.connect)

    def connect(self):
        raise NotImplementedError('Please implement the "connect" method in derived class')

    def subscribe(self, *args):
        raise NotImplementedError('Please implement the "subscribe" method in derived class')

    def on_message(self, topic, payload, qos, dup, retain, msgId):
        raise NotImplementedError('Please implement the "on_message" method in derived class or pass a callable using the "callback" constructor argument')

    def on_error(self, *args):
        log.error("ERROR: args={args!s}", args=args)

    """
    def _todo_publish(self):
        d = self.protocol.publish(topic="foo/bar/baz", message="hello friends")
        d.addErrback(self.on_error)

    def _todo_prepareToPublish(self, *args):
        self.task = task.LoopingCall(self.publish)
        self.task.start(5.0)
    """
