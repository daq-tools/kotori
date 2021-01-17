# -*- coding: utf-8 -*-
"""
Kotori is a data acquisition, routing and graphing toolkit
Copyright (C) 2014-2021 Andreas Motl, <andreas@getkotori.org>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from pkg_resources import EntryPoint
from pyramid.settings import asbool
from twisted.logger import Logger, LogLevel
from kotori.util.configuration import read_list
from kotori.util.errors import last_error_and_traceback
from kotori.util.logger import changeLogLevel
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

        if not factory:
            return

        try:
            application_settings = self.settings[name]
            application = factory(name=name, application_settings=application_settings, global_settings=self.settings)
            application.startService()
        except Exception as ex:
            log.failure('Error running application factory "{name}":\n{log_failure}', name=name)
            return

    def get_application_factory(self, name):

        # Get application information from configuration object
        try:
            application_settings = self.settings[name]
            app_factory = \
                'app_factory' in application_settings and \
                application_settings.app_factory or \
                application_settings.application
        except:
            log.failure('Application configuration object for "{name}" not found, missing setting "app_factory"', name=name)
            return

        try:
            factory_callable = self.load_entrypoint(app_factory)
        except:
            log.failure('Error loading application entrypoint "{app_factory}" for "{name}":\n{ex}',
                name=name, app_factory=app_factory, ex=last_error_and_traceback())
            return

        return factory_callable

    @classmethod
    def load_entrypoint(cls, reference, onerror='raise'):

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
            thing = entrypoint.resolve()
        except:
            log.failure('Error loading entrypoint "{reference}"', reference=reference)
            if onerror == 'raise':
                raise
            elif onerror == 'ignore':
                return cls.noop_callable
            #raise

        return thing

    @classmethod
    def noop_callable(cls, *args, **kwargs):
        pass

    def get_vendors(self):
        for name, config_object in self.settings.items():
            if 'type' in config_object and config_object.type == 'vendor':
                if 'enable' not in config_object or asbool(config_object['enable']):
                    yield name

    def get_applications(self):
        for name, config_object in self.settings.items():
            if 'type' in config_object and config_object.type == 'application':
                if 'enable' not in config_object or asbool(config_object['enable']):
                    yield name

    def boot_vendors(self):
        """
        Boot all enabled vendors.
        """
        vendors = list(self.get_vendors())
        log.info('Enabling vendors {vendors}', vendors=vendors)

        debug = self.settings.options.debug

        for vendor in vendors:
            if hasattr(VendorBootloader, vendor):
                log.info(u'Starting vendor environment for "{vendor}"', vendor=vendor)
                bootloader = getattr(VendorBootloader, vendor)
                try:
                    bootloader(self.settings)
                except Exception as ex:
                    log.failure(
                        'Error booting vendor environment for "{vendor}"":\n{log_failure}"', vendor=vendor)
            else:
                message = 'Vendor environment for "{vendor}" missing.'.format(vendor=vendor)
                log.critical(message)


class VendorBootloader(object):

    @classmethod
    def hydro2motion(cls, settings):
        from kotori.vendor.hydro2motion.database.influx import h2m_boot_influx_database
        from kotori.vendor.hydro2motion.network.udp import h2m_boot_udp_adapter
        from kotori.vendor.hydro2motion.web.server import boot_web

        debug = settings.options.debug
        boot_web(settings, debug=debug)
        h2m_boot_udp_adapter(settings, debug=debug)
        h2m_boot_influx_database(settings)

    @classmethod
    def hiveeyes(cls, settings):
        from kotori.vendor.hiveeyes.application import hiveeyes_boot
        debug = settings.options.debug
        hiveeyes_boot(settings, debug=debug)

    @classmethod
    def lst(cls, settings):
        from kotori.vendor.lst.application import lst_boot
        debug = settings.options.debug
        if settings.options.debug_vendor and 'lst' in read_list(settings.options.debug_vendor):
            changeLogLevel('kotori.vendor.lst', LogLevel.debug)
        lst_boot(settings)
