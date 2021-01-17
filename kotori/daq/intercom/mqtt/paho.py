# -*- coding: utf-8 -*-
# (c) 2016-2021 Andreas Motl <andreas.motl@getkotori.org>
# https://pypi.python.org/pypi/paho-mqtt/
from __future__ import absolute_import
import os
import paho.mqtt.client as mqtt
from twisted.logger import Logger
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from twisted.application.service import Service
from kotori.daq.intercom.mqtt.base import BaseMqttAdapter

log = Logger()


class PahoMqttAdapter(BaseMqttAdapter, Service):

    # If connection fails at first, retry connecting each X seconds
    retry_interval = 5

    def connect(self):
        """
        Connect to MQTT broker.
        """
        # TODO: Check if we can do asynchronous connection establishment.
        #       Currently, this is done synchronously which could harm
        #       other subsystems in timeout or otherwise blocking situations.

        # Make MQTT client identifier even more unique by adding process id
        pid = os.getpid()
        client_id = '{}:{}'.format(self.name, str(pid))

        # Connection establishment
        self.client = mqtt.Client(client_id=client_id, clean_session=True)

        # Optionally authenticate connection
        if self.broker_username:
            self.client.username_pw_set(self.broker_username, self.broker_password)

        # Set event handlers
        self.client.on_connect = lambda *args: reactor.callFromThread(self.on_connect, *args)
        self.client.on_message = lambda *args: reactor.callFromThread(self.on_message, *args)
        self.client.on_log     = lambda *args: reactor.callFromThread(self.on_log, *args)

        # Connect with retry
        self.connect_loop = LoopingCall(self.connect_with_retry)
        self.connect_loop.start(self.retry_interval, now=True)

    def connect_with_retry(self):
        try:
            self.client.connect(self.broker_host, port=self.broker_port, keepalive=60)
            self.connect_loop.stop()
        except:
            log.failure(u'Error connecting to MQTT broker but retrying each {retry_interval} seconds',
                retry_interval=self.retry_interval)
            return

        """
        This is part of the threaded client interface. Call this once to
        start a new thread to process network traffic. This provides an
        alternative to repeatedly calling loop() yourself.
        """
        self.client.loop_start()
        reactor.addSystemEventTrigger('before', 'shutdown', self.client.loop_stop, True)

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        """
        on_connect(client, userdata, flags, rc): called when the broker responds to our connection
          request.
          flags is a dict that contains response flags from the broker:
            flags['session present'] - this flag is useful for clients that are
                using clean session set to 0 only. If a client with clean
                session=0, that reconnects to a broker that it has previously
                connected to, this flag indicates whether the broker still has the
                session information for the client. If 1, the session still exists.
          The value of rc determines success or not:
            0: Connection successful
            1: Connection refused - incorrect protocol version
            2: Connection refused - invalid client identifier
            3: Connection refused - server unavailable
            4: Connection refused - bad username or password
            5: Connection refused - not authorised
            6-255: Currently unused.
        """
        log.debug("Connected to MQTT. userdata={userdata}, flags={flags}, rc={rc}",
            userdata=userdata, flags=flags, rc=rc)

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        #client.subscribe("$SYS/#")
        self.subscribe()

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, message):
        """
        on_message(client, userdata, message): called when a message has been received on a
          topic that the client subscribes to. The message variable is a
          MQTTMessage that describes all of the message parameters.
        """

        # TODO: Do something with "client" object (paho.mqtt.client.Client)

        topic = message.topic
        payload = message.payload

        # Make metadata dictionary to be passed as kwargs later.

        # Mungle topic and payload out of metadata.
        metadata = {}
        for name in message.__slots__:
            try:
                metadata[name] = getattr(message, name)
            except AttributeError:
                pass

        del metadata['_topic']
        del metadata['payload']

        # Mungle userdata into message.
        metadata['userdata'] = userdata

        if not topic.endswith('error.json'):
            log.debug('on_message: name={name}, topic={topic}, payload={payload}, kwargs={kwargs}', name=self.name, topic=topic, payload=payload, kwargs=metadata)

        return self.callback(topic=topic, payload=payload, **metadata)

    def publish(self, topic, payload):
        log.debug(u'Publishing to topic={topic}, payload={payload}', topic=topic, payload=payload)
        return self.client.publish(topic, payload)

    def subscribe(self, *args):
        #d = self.protocol.subscribe("foo/bar/baz", 0)
        log.info(u"Subscribing to topics {subscriptions}. client={client}", subscriptions=self.subscriptions, client=self.client)
        for topic in self.subscriptions:
            log.info(u"Subscribing to topic '{topic}'", topic=topic)
            # Topic name **must not** be unicode, so casting to string
            e = self.client.subscribe(str(topic), qos=0)

    def on_log(self, client, userdata, level, buf):
        """
        on_log(client, userdata, level, buf): called when the client has log information. Define
          to allow debugging. The level variable gives the severity of the message
          and will be one of MQTT_LOG_INFO, MQTT_LOG_NOTICE, MQTT_LOG_WARNING,
          MQTT_LOG_ERR, and MQTT_LOG_DEBUG. The message itself is in buf.
        """
        log.debug(u'{message}. level={level_mqtt}, userdata={userdata}', message=buf, level_mqtt=level, userdata=userdata)
