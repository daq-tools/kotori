# -*- coding: utf-8 -*-
# (c) 2016-2017 Andreas Motl <andreas@getkotori.org>
import threading
from copy import deepcopy
from bunch import Bunch, bunchify
from collections import defaultdict
from pyramid.settings import asbool
from twisted.web import http
from twisted.logger import Logger
from twisted.application.service import MultiService
from kotori.util.configuration import read_list
from kotori.daq.services import RootService, MultiServiceMixin
from kotori.io.protocol.forwarder import ForwarderAddress
from kotori.io.protocol.http import HttpServerService
from kotori.firmware.builder import FirmwareBuilder

"""
Todo
====
- [o] Use threads for running concurrent build operations, but
  safeguard the compilation process using locks around "build_firmware".
"""

log = Logger()

class FirmwareBuilderApplication(RootService):
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
        service = FirmwareBuilderService(
            channel = self.channel
        )

        # Register service component with its container
        self.registerService(service)


class FirmwareBuilderService(MultiService, MultiServiceMixin):

    def __init__(self, channel=None):

        MultiService.__init__(self)

        self.channel = channel or Bunch(realm=None, subscriptions=[])

        self.name = u'service-fb-' + self.channel.get('realm', str(id(self)))

        # A bunch of locks for constraining concurrent
        # make processes on the same directory.
        self.locks = defaultdict(threading.RLock)

    def setupService(self):
        #self.log(log.info, u'Setting up')
        self.settings = self.parent.settings

        log.info('Providing firmware for {repository} at {source}', source=self.channel.source, repository=self.channel.repository)
        self.setupSource()

    def setupSource(self):
        # Configure data source

        # There should be just a single instance of a HTTP server service object
        self.source_service = HttpServerService.create(self.settings)

        # Wrap source channel settings into address object
        self.source_address = ForwarderAddress(self.channel.source)

        # Register URI route representing source channel
        self.source_service.registerEndpoint(
            methods     = self.source_address.predicates,
            path        = self.source_address.uri.path,
            callback    = self.build)

    def build(self, bucket):

        # 1. Map/transform topology address information

        # Transformation dict
        data = {}

        # Update transformation dict with information from url capturing
        data.update(bucket.tdata.copy())

        # Update transformation dict with information from request (body/params)
        data.update(bucket.data)

        # Automatically derive "MQTT_TOPIC" from telemetry channel address information
        if 'MQTT_TOPIC' not in data:
            if 'TELEMETRY_REALM' in data and data['TELEMETRY_REALM']:
                data['MQTT_TOPIC'] = '{TELEMETRY_REALM}/{TELEMETRY_USER}/{TELEMETRY_SITE}/{TELEMETRY_NODE}/data.json'.format(**data)

        # Extract option fields and delete them from transformation dict
        options = Bunch()
        option_fields = ['url', 'ref', 'update_submodules', 'path', 'architecture', 'makefile', 'suffix']
        for field in option_fields:
            if field in data:
                options[field] = data[field]
                del data[field]

        # Sanity checks
        # TODO: Check "options.suffix" for being "hex" or "elf" only

        # Override url option with repo url from settings
        options.url = self.channel.repository

        # Propagate path to ESP_ROOT
        # TODO: Clone from https://github.com/esp8266/Arduino
        options.esp_root = self.channel.esp_root

        # Further "options" manipulations

        # Type coercion with default value
        if 'update_submodules' in options:
            options['update_submodules'] = asbool(options['update_submodules'])
        else:
            options['update_submodules'] = True


        # 2. Reporting
        log.info('Building firmware, options={options}, data={data}', options=dict(options), data=dict(data))


        # 3. Build firmware, capturing error output, if any
        payload = self.build_firmware_safe(bucket=bucket, options=bunchify(options), data=bunchify(data))


        # 4. TODO: Announce to appropriate channel via MQTT

        return payload

    def build_firmware_safe(self, options=None, **kwargs):
        # As a very rough guideline, we take a lock on the parameter obtained as working dir
        # to have exclusively one compiler / make process running in the very same directory.
        with self.locks[options.path]:
            return self.build_firmware(options=options, **kwargs)

    def build_firmware(self, bucket=None, options=None, data=None):

        # FirmwareBuilder machinery
        fwbuilder = FirmwareBuilder(
            repo_url=options.url, repo_branch=options.ref, update_submodules=options.update_submodules,
            workingdir=options.path,
            architecture = options.get('architecture'), esp_root=options.esp_root)

        # Run build process with capturing its output
        with fwbuilder.capture() as result:

            # Acquire source code from git repository
            fwbuilder.acquire_source()

            # Patch files with individual parameters
            """
            data = {
                'BOARD_TAG': 'mega2560',
                'BOARD_SUB': 'atmega2560',
                'HE_USER': 'Hotzenplotz',
                'HE_SITE': 'Buxtehude',
                'HE_HIVE': 'Raeuberhoehle',
                'GPRSBEE_APN': 'internet.altes-land.de',
                'GPRSBEE_VCC': 23,
                }
            """
            patch_files = read_list(self.channel.patch_files)
            fwbuilder.patch_files(patch_files, data)

            # Run build process
            fwbuilder.run_build(makefile=options.makefile)
            artefact = fwbuilder.make_artefact()

        if result.success:

            # Compute extended firmware name suffix from transformation dict
            # TODO: Route this information to "Artefact" object
            """
            fwparams = ''
            if data:
                data = data.copy()
                del data['slot']
                dlist = []
                for key, value in data.iteritems():
                    dlist.append(u'{key}={value}'.format(**locals()))
                fwparams = u'-' + u','.join(dlist)
            """

            filename = '{realm}_{name}.{suffix}'.format(
                realm=self.channel.realm, name=artefact.fullname, suffix=options.suffix)

            log.info(u'Build succeeded, filename: {filename}, artefact: {artefact}', filename=filename, artefact=artefact)

            bucket.request.setHeader('Content-Type', 'application/octet-stream')
            bucket.request.setHeader('Content-Disposition', 'attachment; filename={filename}'.format(filename=filename))

            # "options.suffix" may be "hex" or "elf"
            payload = artefact.get_binary(options.suffix)
            return payload

        else:
            error_message = fwbuilder.error_message()
            log.error(u'Build failed\n{message}', message=error_message)
            bucket.request.setResponseCode(http.BAD_REQUEST)
            bucket.request.setHeader('Content-Type', 'text/plain; charset=utf-8')
            return error_message.encode('utf-8')

    def startService(self):
        self.setupService()
        self.log(log.info, u'Starting')
        MultiService.startService(self)

    def log(self, level, prefix):
        level('{prefix} {class_name}. name={name}, channel={channel}',
            prefix=prefix, class_name=self.__class__.__name__, name=self.name, channel=dict(self.channel))


def boot(name=None, **kwargs):
    app = FirmwareBuilderApplication(name=name, **kwargs)
    return app

