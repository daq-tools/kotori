# -*- coding: utf-8 -*-
# (c) 2015-2021 Andreas Motl <andreas.motl@getkotori.org>
# https://pypi.python.org/pypi/twisted-mqtt
# https://github.com/astrorafael/twisted-mqtt/
from __future__ import absolute_import
from twisted.logger import Logger

log = Logger()


class BaseMqttAdapter(object):

    def __init__(self, name,
                 broker_host=u'localhost', broker_port=1883, broker_username=None, broker_password=None,
                 debug=False, callback=None, subscriptions=None):
        self.name = name
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.broker_username = broker_username
        self.broker_password = broker_password
        self.callback = callback or self.on_message
        self.subscriptions = subscriptions or []

    def startService(self):
        self.log(log.info, u'Starting')
        self.running = 1
        self.connect()
        #reactor.callInThread(self.connect)

    def connect(self):
        raise NotImplementedError('Please implement the "connect" method in derived class')

    def subscribe(self, *args):
        raise NotImplementedError('Please implement the "subscribe" method in derived class')

    def on_message(self, topic=None, payload=None, **kwargs):
        # former def on_message(self, topic, payload, qos, dup, retain, msgId):
        # kwargs: qos, dup, retain, msgId
        raise NotImplementedError('Please implement the "on_message" method in derived class or pass a callable using the "callback" constructor argument')

    def on_error(self, *args):
        log.error("ERROR: args={args!s}", args=args)

    def log(self, callable, prefix):
        callable(u'{prefix} {class_name}. name={name}, broker={broker_host}:{broker_port}, object={repr}',
            prefix=prefix, class_name=self.__class__.__name__,
            name=self.name, repr=repr(self),
            broker_host=self.broker_host, broker_port=self.broker_port)

    """
    def _todo_publish(self):
        d = self.protocol.publish(topic="foo/bar/baz", message="hello friends")
        d.addErrback(self.on_error)

    def _todo_prepareToPublish(self, *args):
        self.task = task.LoopingCall(self.publish)
        self.task.start(5.0)
    """
