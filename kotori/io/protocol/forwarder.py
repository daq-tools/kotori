# -*- coding: utf-8 -*-
# (c) 2016-2021 Andreas Motl <andreas@getkotori.org>
import re

from munch import munchify, Munch
from six.moves.urllib.parse import urlparse
from twisted.logger import Logger
from twisted.application.service import MultiService
from kotori.util.configuration import read_list
from kotori.core import KotoriBootloader
from kotori.daq.services import RootService, MultiServiceMixin
from kotori.io.protocol.http import HttpServerService
from kotori.io.protocol.target import ForwarderTargetService

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
        self.setupChannel(channel=application_settings, name=name)

        # Create application service object composed of subsystem components
        service = ProtocolForwarderService(
            channel = self.channel
        )

        # Register service component with its container
        self.registerService(service)


class ProtocolForwarderService(MultiServiceMixin, MultiService):
    """
    Container service for source and target services.

    Both services are connected unidirectionally via ``forward`` callback.

    As of June 2016, the only source service is a singleton
    instance of a ``HttpServerService``. This might be
    improved by adding more handlers.

    Also, there are currently two target services
    for emitting data, MQTT and InfluxDB.
    """

    def __init__(self, channel=None):
        self.channel = channel or Munch(realm=None, subscriptions=[])
        MultiServiceMixin.__init__(self, name=self.channel.name + '-forwarder')

    def setupService(self):
        #self.log(log.info, u'Setting up')
        log.info(u'Starting {name}'.format(name=self.logname))

        self.settings = self.parent.settings

        # Configure metrics to be collected each X seconds
        #self.metrics = Munch(tx_count=0, starttime=time.time(), interval=2)

        log.info('Forwarding payloads from {source} to {target}', **self.channel)
        self.setupSource()
        self.setupTarget()

    def setupSource(self):
        """
        Configure data source by registering a HTTP endpoint
        using the source address derived from channel settings.
        """

        # There should be just a single instance of a HTTP server service object
        self.source_service = HttpServerService.create(self.settings)

        # Wrap source channel settings into address object
        self.source_address = ForwarderAddress(self.channel.source)

        # Register URI route representing source channel
        self.source_service.registerEndpoint(
            methods     = self.source_address.predicates,
            path        = self.source_address.uri.path,
            callback    = self.forward)

    def setupTarget(self):
        """
        Configure data target by registering a service object
        using the target address derived from channel settings.
        """

        # Wrap target channel into address object
        self.target_address = ForwarderAddress(self.channel.target)
        self.target_uri = self.target_address.uri

        # Compute name for service object, should be unique.
        target_service_name = u'{realm}-{channel_name}'.format(
            realm=self.channel.realm, channel_name=self.channel.name)

        # Register service representing target channel.
        # Each service should just run once, so they are named to be found again.
        # TODO: Add sanity checks for collisions here.
        try:
            self.target_service = self.getServiceNamed(target_service_name)
        except KeyError:
            self.target_service = ForwarderTargetService(name=target_service_name, address=self.target_address)
            self.registerService(self.target_service)

    def forward(self, bucket):
        """
        Receive data bucket from source, run through
        transformation machinery and emit to target.
        """

        # 1. Map/transform topology address information
        if 'transform' in self.channel:
            for entrypoint in read_list(self.channel.transform):
                try:
                    transformer = KotoriBootloader.load_entrypoint(entrypoint)
                    bucket.tdata.update(transformer(bucket.tdata))
                except ImportError as ex:
                    log.error('ImportError "{message}" when loading entrypoint "{entrypoint}"',
                        entrypoint=entrypoint, message=ex)

        # MQTT doesn't prefer leading forward slashes with topic names, let's get rid of them
        target_uri_tpl = self.target_uri.path.lstrip('/')

        # Compute target bus topic from url matches
        target_uri = target_uri_tpl.format(**bucket.tdata)

        # Enrich bucket by putting source and target addresses into it
        bucket.address = Munch(source=self.source_address, target=self.target_address)

        # 2. Reporting
        bucket_logging = Munch(bucket)
        if 'body' in bucket_logging and len(bucket_logging.body) > 100:
            bucket_logging.body = bucket_logging.body[:100] + b' [...]'
        log.debug('Forwarding bucket to {target} with bucket={bucket}. Effective target uri is {target_uri}',
            target=self.channel.target, target_uri=target_uri, bucket=dict(bucket_logging))

        # 3. Adapt, serialize and emit appropriately
        return self.target_service.emit(target_uri, bucket)

    def log(self, level, prefix):
        level('{prefix} {class_name}. name={name}, channel={channel}',
            prefix=prefix, class_name=self.__class__.__name__, name=self.name, channel=dict(self.channel))


class ForwarderAddress(object):
    """
    Addresses are made of uris and predicates, e.g.::

        http:/api/mqttkit-1/{address:.*}/data [POST]
        ^                                      ^
        |                                      |
        ----- uri                   predicate --

    Synopsis:

    >>> address = ForwarderAddress(u'http:/api/mqttkit-1/{address:.*}/data [POST]')

    >>> address.uri.scheme
    'http'

    >>> address.uri.path
    '/api/mqttkit-1/{address:.*}/data'

    >>> address.predicates
    ['POST']
    """

    address_pattern = re.compile('^(?P<uri>.*?)(?: \[(?P<predicates>.+)\])?$')

    def __init__(self, address):
        self.raw_uri = None
        self.raw_predicates = None
        self.parsed_uri = None
        self.uri = None
        self.predicates = []
        self.parse(address)

    def parse(self, address):
        m = self.address_pattern.match(address)

        match = m.groupdict()
        if match:
            self.raw_uri = match['uri']
            self.raw_predicates = match['predicates']

            self.parsed_uri = urlparse(self.raw_uri)
            #print("asdict:", munchify(self.parsed_uri._asdict()))
            self.uri = munchify(self.parsed_uri._asdict())
            if self.raw_predicates:
                self.predicates = read_list(self.raw_predicates)

    def __repr__(self):
        return u'{uri} {predicates}'.format(uri=self.parsed_uri.geturl(), predicates=self.predicates)


def boot(name=None, **kwargs):
    app = ProtocolForwarderApplication(name=name, **kwargs)
    return app

