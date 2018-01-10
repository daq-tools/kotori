# -*- coding: utf-8 -*-
# (c) 2015-2017 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
from bunch import Bunch
from collections import OrderedDict
from twisted.logger import Logger
from kotori.daq.services import RootService
from kotori.daq.services.mig import MqttInfluxGrafanaService
from kotori.daq.intercom.strategies import WanBusStrategy
from kotori.daq.graphing.grafana import GrafanaManager

log = Logger()

class HiveeyesGrafanaManager(GrafanaManager):

    knowledge = [
        {'name': 'temperature', 'prefixes': ['temp', 'Temp'],   'suffixes': ['temp', 'temperature'],    'format': 'celsius'},
        {'name': 'humidity',    'prefixes': ['hum'],            'suffixes': ['hum', 'humidity'],        'format': 'humidity'},
        {'name': 'weight',      'prefixes': ['wght', 'weight', 'Gewicht', 'Weight'],    'label':  'kg'},
        {'name': 'volume',      'prefixes': ['volume'],                                 'label':  'dB', 'scale': 10},
    ]

    def get_rule(self, fieldnames):
        """
        Filter knowledgebase by prefix.
        Obtains a list of fieldnames / fieldname prefixes and
        also matches against a list of fieldname prefixes,
        hence the nested loops.
        """

        if not fieldnames:
            return {}

        for rule in self.knowledge:
            for prefix in rule['prefixes']:
                for fieldname in fieldnames:
                    if fieldname.startswith(prefix):
                        return rule

        return {}

    def get_panel_options(self, data, fieldnames):
        return self.get_rule(fieldnames)

    def panel_title_prefix(self, fieldnames):
        return self.get_rule(fieldnames).get('name')

    def get_distinct_panel_field_prefixes(self, data):
        """
        Compute list of fieldname prefixes in order of knowledgebase
        for providing stable input to the panel generator.
        """

        prefixes = OrderedDict()
        fields_given = data.keys()
        fields_used = []
        for rule in self.knowledge:
            for prefix in rule['prefixes']:
                for fieldname in fields_given:
                    if fieldname.startswith(prefix):
                        key = '-'.join(rule['prefixes'])
                        prefixes[key] = rule['prefixes']
                        fields_used.append(fieldname)

            if 'suffixes' in rule:
                for suffix in rule['suffixes']:
                    for fieldname in fields_given:
                        if fieldname.endswith(suffix):
                            key = '-'.join(rule['prefixes'])
                            prefixes[key] = rule['suffixes']
                            fields_used.append(fieldname)

        # Add unused fields
        fields_unused = list(set(fields_given) - set(fields_used))
        if fields_unused:
            prefixes['misc'] = fields_unused

        return prefixes.values()

    def panel_generator(self, storage_location, data, topology):
        """
        Generate Hiveeyes-specific Grafana panels, which is:
        Group multiple temperature or humidity sensors into a single panel (aka. one panel per sensor family),
        even when transmitted in BERadio-specific shortcut notation like 'temp1', 'temp2', etc.
        """

        panels = []

        for prefixes in self.get_distinct_panel_field_prefixes(data):
            panel = self.get_panel_data(storage_location, topology, data, fieldname_prefixes=prefixes)
            panels.append(panel)

        return panels


def hiveeyes_boot(settings, debug=False):

    # Service container root
    rootService = RootService(settings=settings)

    channel = Bunch(**settings.hiveeyes)

    # Main application service
    service = MqttInfluxGrafanaService(
        channel  = channel,
        graphing = HiveeyesGrafanaManager(settings=settings, channel=channel),
        strategy = WanBusStrategy())

    rootService.registerService(service)
    rootService.startService()

