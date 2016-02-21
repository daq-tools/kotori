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
        """
        Decode MQTT topic segments implementing the »quadruple hierarchy strategy«.

        The topology hierarchy is directly specified by the MQTT topic and is
        made up of a minimum of four identifiers describing the core structure::

            realm / network / gateway / node

        The topology identifiers are specified as:

            - "realm" is the designated root realm. You should prefix the topic name
              with this label when opting in for all features of the telemetry platform.
              For other purposes, feel free to publish to any MQTT topic you like.

            - "network" is your personal realm. Choose anything you like or use an
              `Online GUID Generator <https://www.guidgenerator.com/>`_ to gain
              maximum uniqueness.

            - "gateway" is your gateway identifier. Choose anything you like.
              This does not have to be very unique, so you might use labels
              having the names of sites. While you are the owner of this
              namespace hierarchy, remember these labels might be visible on
              the collaborative ether, though.
              So the best thing would be to give kind of nicknames to your
              sites which don't identify their location.

            - "1" is your node identifier. Choose anything you like. This usually
              gets transmitted from an embedded device node. Remember one device node
              might have multiple sensors attached, which is beyond the scope of the
              collection platform: We just accept bunches of named measurement values,
              no matter which sensors they might originate from.
              In other words: We don't need nor favor numeric sensor identifiers,
              let's give them names!
        """

        # regular expression pattern for decoding MQTT topic address segments
        pattern = r'^(?P<realm>.+?)/(?P<network>.+?)/(?P<gateway>.+?)/(?P<node>.+?)(?:/(?P<kind>.+?))?$'

        # decode the topic
        p = re.compile(pattern)
        m = p.match(topic)
        if m:
            address = Bunch(m.groupdict())
        else:
            address = {}

        return address


    def topology_to_database(self, topology):
        """
        Encode topology segment identifiers to database address.

        A database server usually has the concept of multiple databases,
        each with multiple tables. With other databases than RDBMS,
        they might be named differently, but the concept in general
        is the same.

        When mapping the topology quadruple (realm, network, gateway, node) in the form of:

            - realm + network = database name
            - gateway + node  = table name

        We have a perfect fit for computing the slot where to store the measurements.

        """
        # TODO: investigate using tags additionally to / instead of database.series
        sanitize = self.sanitize_db_identifier
        database = Bunch({
            'database': '{}_{}'.format(sanitize(topology.realm), sanitize(topology.network)),
            'series':   '{}_{}'.format(sanitize(topology.gateway), sanitize(topology.node)),
        })
        return database


    @staticmethod
    def sanitize_db_identifier(value):
        """
        Different databases accept different special
        characters as database- or table names.

        Better safe than sorry, let's strip them all.
        """
        value = value.replace('/', '_').replace('.', '_').replace('-', '_')
        return value


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



def hiveeyes_boot(config, debug=False):
    ha = HiveeyesApplication(config)
