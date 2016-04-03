# -*- coding: utf-8 -*-
# (c) 2015-2016 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
from bunch import Bunch
from twisted.logger import Logger
from kotori.daq.services import RootService
from kotori.daq.services.mig import MqttInfluxGrafanaService
from kotori.daq.intercom.strategies import WanBusStrategy
from kotori.daq.graphing.grafana import GrafanaManager

log = Logger()

class HiveeyesGrafanaManager(GrafanaManager):

    def get_panel_options(self, data, fieldname):
        knowledge = [
            {'prefixes': ['temp'],           'format': 'celsius'},
            {'prefixes': ['hum'],            'format': 'humidity'},
            {'prefixes': ['wght', 'weight'], 'label':  'kg'},
            {'prefixes': ['volume'],         'label':  'dB', 'scale': 10},
        ]
        for rule in knowledge:
            for prefix in rule['prefixes']:
                if fieldname.startswith(prefix):
                    return rule

        return {}

    def get_panel_data(self, data, title, fieldname_prefix):
        panel = {'title': title, 'fieldnames': self.collect_fields(data, fieldname_prefix)}
        panel.update(self.get_panel_options(data, fieldname_prefix))
        return panel

    def panel_generator(self, database, series, data, topology):
        """
        Generate fine Grafana panels
        """

        panels = []

        # multi-field panels v1: naive / BERadio-specific
        # detect this payload flavor by checking whether field names have
        # the signature of being sent from a BERadio transmitter
        if 'temp1' in data or 'hum1' in data or 'wght1' in data:
            if 'temp1' in data:
                panels.append(self.get_panel_data(data, 'temperature', 'temp'))
            if 'hum1' in data:
                panels.append(self.get_panel_data(data, 'humidity', 'hum'))
            if 'wght1' in data:
                panels.append(self.get_panel_data(data, 'weight', 'wght'))

        # regular panels: one panel per field
        # c-base amendments
        else:
            for fieldname in sorted(data.keys()):
                panels.append(self.get_panel_data(data, fieldname, fieldname))

        return panels

    def row_title(self, database, series, topology):
        if 'node' in topology and 'gateway' in topology:
            row_title = self.panel_title_suffix(database, series, topology)
            if 'network' in topology:
                row_title += ',net={network}'.format(**topology)
            return row_title

    def panel_title_suffix(self, database, series, topology):
        if 'node' in topology and 'gateway' in topology:
            return 'node={node},gw={gateway}'.format(**topology)



def hiveeyes_boot(settings, debug=False):

    # Service container root
    rootService = RootService(settings=settings)

    # TODO: read from config
    service = MqttInfluxGrafanaService(
        settings,
        channel         = Bunch(**settings.hiveeyes),
        graphing        = HiveeyesGrafanaManager(settings),
        store_strategy  = WanBusStrategy())

    rootService.addService(service)
    #rootService.registerService(service)
    rootService.startService()
