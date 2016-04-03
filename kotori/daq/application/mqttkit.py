# -*- coding: utf-8 -*-
# (c) 2015-2016 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
from bunch import Bunch
from twisted.internet import reactor
from twisted.logger import Logger
from kotori.daq.services import RootService
from kotori.daq.services.mig import MqttInfluxGrafanaService
from kotori.daq.intercom.strategies import WanBusStrategy
from kotori.daq.graphing.grafana import GrafanaManager

log = Logger()

# Service container root
class MqttKitApplication(RootService):

    name = u'MigApplication'

    def setup(self):
        settings = self.settings
        service = MqttInfluxGrafanaService(
            settings,
            channel         = Bunch(**settings.mqttkit),
            graphing        = GrafanaManager(settings),
            store_strategy  = WanBusStrategy())

        self.addService(service)
        #self.registerService(service)


def boot_mqttkit_application(settings):
    app = MqttKitApplication(settings=settings)
    app.setup()
    app.startService()
