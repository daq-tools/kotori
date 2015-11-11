# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import re
from bunch import Bunch
from ConfigParser import ConfigParser
from twisted.logger import Logger
from kotori.daq.application.beradio import BERadioNetworkApplication
from kotori.daq.graphing.grafana import GrafanaManager

logger = Logger()

class HiveeyesApplication(BERadioNetworkApplication):


    def __init__(self, config):

        logger.info('Starting HiveeyesApplication')

        BERadioNetworkApplication.__init__(self, config)

        # mqtt configuration
        self.realm = 'hiveeyes'
        self.subscriptions = [self.realm + '/#']

        # grafana setup
        self.graphing = HiveeyesGrafanaManager(self.config_dict())

        # generic setup
        self.setup()

    def config_dict(self):
        # serialize section-based ConfigParser contents into nested dict
        # TODO: refactor
        if isinstance(self.config, ConfigParser):
            config = {}
            for section in self.config.sections():
                config[section] = dict(self.config.items(section))
            return config

        else:
            return self.config


    def topic_to_topology(self, topic):

        pattern = r'^(?P<realm>.+?)/(?P<network>.+?)/(?P<gateway>.+?)/(?P<node>.+?)(?:/(?P<kind>.+?))?$'
        p = re.compile(pattern)
        m = p.match(topic)

        if m:
            address = Bunch(m.groupdict())
        else:
            address = {}

        return address

    def topology_to_database(self, topology):
        sanitize = self.sanitize_db_identifier
        database = Bunch({
            'database': '{}_{}'.format(sanitize(topology.realm), sanitize(topology.network)),
            'series':   '{}_{}'.format(sanitize(topology.gateway), sanitize(topology.node)),
        })
        return database

    @staticmethod
    def sanitize_db_identifier(value):
        value = value.replace('/', '_').replace('.', '_').replace('-', '_')
        return value


class HiveeyesGrafanaManager(GrafanaManager):

    def panel_generator(self, database, series, data):
        # generate panels
        panels = []
        if 'temp1' in data:
            panels.append({'title': 'temp',      'fieldnames': self.collect_fields(data, 'temp'), 'format': 'celsius'})
        if 'hum1' in data:
            panels.append({'title': 'humidity',  'fieldnames': self.collect_fields(data, 'hum')})
        if 'wght1' in data:
            panels.append({'title': 'weight',    'fieldnames': self.collect_fields(data, 'wght'), 'label': 'kg'})

        return panels


def hiveeyes_boot(config, debug=False):
    ha = HiveeyesApplication(config)
