# -*- coding: utf-8 -*-
# (c) 2014-2016 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
from pkg_resources import EntryPoint
from twisted.logger import Logger
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
        applications = read_list(self.settings.applications.enable)
        log.info('Enabling applications {applications}', applications=applications)
    
        for name in applications:
            self.boot_application(name)

    def boot_application(self, name):
        """
        Boot application defined by configuration
        """
        log.info(u'Starting application "{name}"', name=name)

        # Get application information from configuration object
        try:
            application_settings = self.settings[name]
            app_factory = application_settings.app_factory
        except KeyError:
            log.failure(u'Application configuration object "{name}" not available', name=name)
            return

        # Resolve entrypoint
        entrypoint_source = u'app-entrypoint-{name} = {app_factory}'.format(name=name, app_factory=app_factory)
        entrypoint = EntryPoint.parse(entrypoint_source)
        factory_callable = entrypoint.load(require=False)

        # Initialize application and run as Twisted service
        application = factory_callable(name=name, application_settings=application_settings, global_settings=self.settings)
        application.startService()

    def boot_vendors(self):
        """
        Boot all enabled vendors
        """
        vendors = read_list(self.settings.vendors.enable)
        log.info('Enabling vendors {vendors}', vendors=vendors)
    
        debug = self.settings.options.debug
    
        if 'hydro2motion' in vendors:
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
            lst_boot(self.settings)
