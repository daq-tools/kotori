# -*- coding: utf-8 -*-
# (c) 2016 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
from copy import deepcopy
from urlparse import urlparse
from bunch import Bunch, bunchify
from twisted.application.service import MultiService
from twisted.logger import Logger
from kotori.daq.services import RootService, MultiServiceMixin
from kotori.io.protocol.http import HttpServerService
from kotori.daq.intercom.mqtt import MqttAdapter

log = Logger()

class ProtocolForwarderApplication(RootService):
    """
    Application service container root object
    """

    def __init__(self, name=None, application_settings=None, global_settings=None):
        RootService.__init__(self, settings=global_settings)

        # Compute name for Twisted service
        self.name = u'app-{name}'.format(name=name)

        # Make channel object from application settings configuration object
        application_settings = deepcopy(application_settings)
        application_settings.update(name=name)
        self.channel = Bunch(**application_settings)

        # Create application service object composed of subsystem components
        service = ProtocolForwarderService(
            channel = self.channel
        )

        # Register service component with its container
        self.registerService(service)


class ProtocolForwarderService(MultiService, MultiServiceMixin):

    def __init__(self, channel=None):

        MultiService.__init__(self)

        self.channel = channel or Bunch(realm=None, subscriptions=[])

        self.name = u'service-pf-' + self.channel.get('realm', unicode(id(self)))

    def setupService(self):
        #self.log(log.info, u'Setting up')
        self.settings = self.parent.settings

        # Configure metrics to be collected each X seconds
        #self.metrics = Bunch(tx_count=0, starttime=time.time(), interval=2)

        log.info('Forwarding payloads from {source} to {target}', **self.channel)
        self.setupSource()
        self.setupTarget()

    def setupSource(self):
        # Configure data source

        # There should be just a single instance of a HTTP server service object
        self.source_service = HttpServerService.create(self.settings)

        # Register URI route representing source channel
        self.source_uri = bunchify(urlparse(self.channel.source)._asdict())
        self.source_service.registerEndpoint(path=self.source_uri.path, callback=self.forward)

    def setupTarget(self):
        # Configure data target
        self.settings.mqtt.setdefault('host', u'localhost')
        self.settings.mqtt.setdefault('port', u'1883')
        self.settings.mqtt.setdefault('debug', u'false')

        self.target_uri = bunchify(urlparse(self.channel.target)._asdict())

        target_service_name = u'mqtt-{realm}-{channel_name}'.format(
            realm=self.channel.realm, channel_name=self.channel.name)
        try:
            self.target_service = self.getServiceNamed(target_service_name)
        except KeyError:
            self.target_service = MqttAdapter(
                name          = target_service_name,
                broker_host   = self.settings.mqtt.host,
                broker_port   = int(self.settings.mqtt.port))
            self.registerService(self.target_service)

    def forward(self, bucket):

        # 1. Map/transform topology address information

        # MQTT doesn't prefer leading forward slashes with topic names, let's get rid of them
        target_uri_tpl = self.target_uri.path.lstrip('/')

        # Compute target bus topic from url matches
        target_uri = target_uri_tpl.format(**bucket.match)

        # 2. Reporting
        log.info('Forwarding bucket to {target} with bucket={bucket}. Effective target uri is {target_uri}',
            target=self.channel.target, target_uri=target_uri, bucket=dict(bucket))

        # 3. Adapt, serialize and emit appropriately
        topic   = target_uri
        payload = bucket.payload
        self.target_service.publish(topic, payload)

    def startService(self):
        self.setupService()
        self.log(log.info, u'Starting')
        MultiService.startService(self)
        #self.metrics_twingo = LoopingCall(self.process_metrics)
        #self.metrics_twingo.start(self.metrics.interval, now=False)

    def log(self, level, prefix):
        level('{prefix} {class_name}. name={name}, channel={channel}',
            prefix=prefix, class_name=self.__class__.__name__, name=self.name, channel=dict(self.channel))


def boot(name=None, **kwargs):
    app = ProtocolForwarderApplication(name=name, **kwargs)
    return app

