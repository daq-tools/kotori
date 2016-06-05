# -*- coding: utf-8 -*-
# (c) 2015-2016 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
from bunch import Bunch
from twisted.logger import Logger
from kotori.daq.services import RootService
from kotori.daq.services.mig import MqttInfluxGrafanaService
from kotori.daq.intercom.strategies import WanBusStrategy
from kotori.daq.graphing.grafana import GrafanaManager

log = Logger()

class MqttKitApplication(RootService):
    """
    Application service container root object
    """

    def __init__(self, name=None, application_settings=None, global_settings=None):
        RootService.__init__(self, settings=global_settings)

        # Compute name for Twisted service
        self.name = u'app-{name}'.format(name=name)

        # Make channel object from application settings configuration object
        self.channel = Bunch(**application_settings)

        # Create application service object composed of subsystem components
        service = MqttInfluxGrafanaService(
            channel  = self.channel,
            # Data processing strategy and graphing components
            strategy = WanBusStrategy(),
            graphing = GrafanaManager(global_settings)
            )

        # Register service component with its container
        self.registerService(service)


def mqttkit_application(name=None, **kwargs):
    app = MqttKitApplication(name=name, **kwargs)
    return app
