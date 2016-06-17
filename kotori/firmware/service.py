# -*- coding: utf-8 -*-
# (c) 2016 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
from copy import deepcopy
from urlparse import urlparse
from bunch import Bunch, bunchify
from twisted.web import http
from twisted.logger import Logger
from twisted.application.service import MultiService
from kotori.configuration import read_list
from kotori.daq.services import RootService, MultiServiceMixin
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

        self.name = u'service-fb-' + self.channel.get('realm', unicode(id(self)))

    def setupService(self):
        #self.log(log.info, u'Setting up')
        self.settings = self.parent.settings

        log.info('Providing firmware for {target} at {source}', **self.channel)
        self.setupSource()

    def setupSource(self):
        # Configure data source

        # There should be just a single instance of a HTTP server service object
        self.source_service = HttpServerService.create(self.settings)

        # Register URI route representing source channel
        self.source_uri = bunchify(urlparse(self.channel.source)._asdict())
        self.source_service.registerEndpoint(path=self.source_uri.path, callback=self.build)

    def build(self, bucket):

        # 1. Map/transform topology address information

        # Transformation dict
        data = {}

        # Update transformation dict with information from url capturing
        data.update(bucket.match.copy())

        # Update transformation dict with information from request (body/params)
        data.update(bucket.data)

        # Extract option fields and delete them from transformation dict
        options = Bunch()
        option_fields = ['url', 'ref', 'path', 'makefile', 'suffix']
        for field in option_fields:
            if field in data:
                options[field] = data[field]
                del data[field]

        # Override url option with repo url from settings
        options.url = self.channel.repository


        # 2. Reporting
        log.info('Building firmware, options={options}, data={data}', options=dict(options), data=dict(data))


        # 3. Build firmware, capturing error output, if any
        #print 'bucket:'; pprint(bucket)
        return self.build_firmware(bucket, bunchify(options), bunchify(data))

    def build_firmware(self, bucket, options, data):

        # Sanity checks
        # TODO: Check "options.suffix" for being "hex" or "elf" only

        # FirmwareBuilder machinery
        fwbuilder = FirmwareBuilder(repo_url=options.url, repo_branch=options.ref, workingdir=options.path)

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
            fwparams = ''
            if data:
                dlist = []
                for key, value in data.iteritems():
                    dlist.append(u'{key}={value}'.format(**locals()))
                fwparams = u'-' + u','.join(dlist)

            log.info(u'Build succeeded, artefact: {artefact}', artefact=artefact)
            bucket.request.setHeader('Content-Type', 'application/octet-stream')
            bucket.request.setHeader('Content-Disposition',
                'attachment; filename={realm}_{name}{fwparams}.{suffix}'.format(
                realm=self.channel.realm, name=artefact.fullname, fwparams=fwparams, suffix=options.suffix))

            # "options.suffix" may be "hex" or "elf"
            payload = getattr(artefact, options.suffix)
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

