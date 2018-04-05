# -*- coding: utf-8 -*-
# (c) 2018 Andreas Motl <andreas@getkotori.org>
from pprint import pprint

from bunch import Bunch
from kotori.daq.services import RootService, MultiServiceMixin
from twisted.application.service import MultiService
from twisted.internet.task import LoopingCall
from twisted.logger import Logger

log = Logger()


class GrafanaMaintenanceApplication(RootService):
    """
    Application service container root object
    for hosting Grafana maintanance tasks.
    """

    def __init__(self, name=None, application_settings=None, global_settings=None):
        RootService.__init__(self, settings=global_settings)

        # Compute name for Twisted service
        self.name = u'app-{name}'.format(name=name)

        # Make channel object from application settings configuration object
        self.setupChannel(settings=application_settings, name=name)

        # Create application service object composed of subsystem components
        if 'dashboard_refresh_taming' in self.channel and self.channel.dashboard_refresh_taming:
            if self.channel.dashboard_refresh_taming == 'true':
                self.channel.dashboard_refresh_taming = 'standard'

                service = DashboardRefreshTamingService(
                    channel=self.channel
                )

                # Register service component with its container
                self.registerService(service)


class DashboardRefreshTamingService(MultiServiceMixin, MultiService):
    """
    Service for taming the refresh interval of Grafana dashboards.
    """

    def __init__(self, channel=None, preset='standard'):
        self.channel = channel or Bunch()
        self.preset = preset
        #MultiServiceMixin.__init__(self, name=self.channel.name + '-dashboard-tamer')
        MultiService.__init__(self)

    def setupService(self):
        log.info(u'Setting up {name}', name=self.logname)
        #self.settings = self.parent.settings

    def startService(self):
        self.setupService()
        self.log(log.info, u'Starting')
        MultiService.startService(self)
        self.tamer_twingo = LoopingCall(self.process_dashboards)
        self.tamer_twingo.start(3, now=True)

    def process_dashboards(self):
        self.parent.grafana_api.tame_refresh_interval(preset=self.preset)


def boot_service(name=None, **kwargs):
    app = GrafanaMaintenanceApplication(name=name, **kwargs)
    return app
