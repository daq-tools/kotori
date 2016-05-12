# -*- coding: utf-8 -*-
# (c) 2014-2016 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
from pkg_resources import EntryPoint
from pyramid.settings import asbool
from twisted.logger import Logger, LogLevel
from kotori.logger import changeLogLevel
from kotori.configuration import read_list
from kotori.version import __VERSION__

log = Logger()
APP_NAME = u'Kotori version ' + __VERSION__

# TODO: introduce kotori.core.boot_component(s)

class KotoriBootloader(object):

    def __init__(self, settings=None):
        self.settings = settings

    def boot_applications(self):
        """
        Boot all enabled applications
        """
        applications = list(self.get_applications())
        log.info(u'Enabling applications {applications}', applications=applications)
        for name in applications:
            self.boot_application(name)

    def boot_application(self, name):
        """
        Boot application defined by configuration
        """
        log.info(u'Starting application "{name}"', name=name)

        # Initialize application and run as Twisted service
        factory = self.get_application_factory(name)
        if factory:
            application_settings = self.settings[name]
            application = factory(name=name, application_settings=application_settings, global_settings=self.settings)
            application.startService()

    def get_application_factory(self, name):

        # Get application information from configuration object
        try:
            application_settings = self.settings[name]
            app_factory = application_settings.app_factory
        except:
            log.failure('Application configuration object "{name}" not found', name=name)
            return

        try:
            factory_callable = self.load_entrypoint(app_factory)
        except:
            log.failure('Application entrypoint "{app_factory}" for "{name}" not loaded', name=name, app_factory=app_factory)
            return

        return factory_callable

    @classmethod
    def load_entrypoint(cls, reference):

        # Resolve entrypoint
        expression = u'_ = {reference}'.format(reference=reference)
        try:
            entrypoint = EntryPoint.parse(expression)
        except:
            log.failure('Error parsing entrypoint "{reference}" from expression "{expression}"',
                reference=reference, expression=expression)
            raise

        # Load entrypoint
        try:
            thing = entrypoint.load(require=False)
        except:
            log.failure('Error loading entrypoint "{reference}"', reference=reference)
            raise

        return thing

    def get_vendors(self):
        for name, config_object in self.settings.iteritems():
            if 'type' in config_object and config_object.type == 'vendor':
                if 'enable' not in config_object or asbool(config_object['enable']):
                    yield name

    def get_applications(self):
        for name, config_object in self.settings.iteritems():
            if 'type' in config_object and config_object.type == 'application':
                if 'enable' not in config_object or asbool(config_object['enable']):
                    yield name

    def boot_vendors(self):
        """
        Boot all enabled vendors
        """
        vendors = list(self.get_vendors())
        log.info('Enabling vendors {vendors}', vendors=vendors)
    
        debug = self.settings.options.debug
    
        if 'hydro2motion' in vendors:
            #log.info(u'Starting vendor "{name}"', name=name)
            from kotori.vendor.hydro2motion.database.influx import h2m_boot_influx_database
            from kotori.vendor.hydro2motion.network.udp import h2m_boot_udp_adapter
            from kotori.vendor.hydro2motion.web.server import boot_web
            boot_web(self.settings, debug=debug)
            h2m_boot_udp_adapter(self.settings, debug=debug)
            h2m_boot_influx_database(self.settings)
    
        if 'hiveeyes' in vendors:
            from kotori.vendor.hiveeyes.application import hiveeyes_boot
            hiveeyes_boot(self.settings, debug=debug)

        if 'lst' in vendors:
            from kotori.vendor.lst.application import lst_boot
            if self.settings.options.debug_vendor and 'lst' in read_list(self.settings.options.debug_vendor):
                changeLogLevel('kotori.vendor.lst', LogLevel.debug)
            lst_boot(self.settings)
