# -*- coding: utf-8 -*-
# (c) 2015-2021 The Hiveeyes Developers <hello@hiveeyes.org>
import re
import json

import attr
from bunch import Bunch
from collections import OrderedDict

from grafana_api_client import GrafanaPreconditionFailedError, GrafanaClientError
from pkg_resources import resource_filename
from jinja2 import Template
from twisted.logger import Logger
from kotori.daq.services import RootService
from kotori.daq.services.mig import MqttInfluxGrafanaService
from kotori.daq.strategy.wan import WanBusStrategy
from kotori.daq.graphing.grafana.manager import GrafanaManager
from kotori.util.common import SmartBunch

log = Logger()


class HiveeyesGenericGrafanaManager(GrafanaManager):

    knowledge = [
        {'name': 'temperature', 'prefixes': ['temp', 'Temp'],   'suffixes': ['temp', 'temperature'],    'format': 'celsius'},
        {'name': 'humidity',    'prefixes': ['hum'],            'suffixes': ['hum', 'humidity'],        'format': 'humidity'},
        {'name': 'weight',      'prefixes': ['wght', 'weight', 'Gewicht', 'Weight'],    'label':  'kg'},
        {'name': 'volume',      'prefixes': ['volume'],                                 'label':  'dB', 'scale': 10},
    ]

    def get_dashboard_identity(self, storage_location, topology=None):

        # Compute effective topology information
        topology = topology or {}
        realm = topology.get('realm', 'default')
        network = topology.get('network', storage_location.database)

        # Derive dashboard uid and name from topology information
        identity = SmartBunch(
            uid=u'{realm}-{network}-instant'.format(realm=realm, network=network),
            name=u'{realm}-{network}'.format(realm=realm, network=network),
            title=u'{realm}-{network}'.format(realm=realm, network=network),
            # TODO: Use real title after fully upgrading to new Grafana API (i.e. don't use get-by-slug anymore!)
            #title=u'Hiveeyes Rohdaten im Netzwerk ' + network,
        )
        #print identity.prettify()

        return identity

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
        fields_given = list(data.keys())
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

        return list(prefixes.values())

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


class HiveeyesBeehiveGrafanaManager(GrafanaManager):

    def __init__(self, *args, **kwargs):
        GrafanaManager.__init__(self, *args, **kwargs)
        self.tpl_dashboard_weef = self.get_template('grafana-dashboard-weef-de.json')

    def get_template(self, filename):
        return Template(open(resource_filename('kotori.vendor.hiveeyes', filename), "rb").read().decode('utf-8'))

    def get_dashboard_identity(self, storage_location, topology=None):

        # Compute effective topology information
        topology = topology or {}
        realm = topology.get('realm', 'default')
        network = topology.get('network', storage_location.database)

        # Derive dashboard uid and name from topology information
        nodename = u'{gateway} / {node}'.format(gateway=topology.gateway, node=topology.node)
        identity = SmartBunch(
            #uid=u'{realm}-{network}-instant'.format(realm=realm, network=network),
            name=self.strategy.topology_to_label(topology),
            title=self.strategy.topology_to_label(topology),
            # TODO: Use real title after fully upgrading to new Grafana API (i.e. don't use get-by-slug anymore!)
            # title=u'Hiveeyes Umweltcockpit für Meßknoten {nodename} im Netzwerk {network}'.format(nodename=nodename, network=network),
            # title=u'Hiveeyes Ertragscockpit für Meßknoten {nodename} im Netzwerk {network}'.format(nodename=nodename, network=network),
        )
        #print identity.prettify()

        return identity

    def provision(self, storage_location, message, topology):

        topology = topology or {}

        # The identity information of this provisioning process
        dashboard_identity = self.get_dashboard_identity(storage_location, topology)
        signature = (storage_location.database, storage_location.measurement)
        whoami = 'dashboard "{dashboard_name}" for database "{database}" and measurement "{measurement}"'.format(
            dashboard_name=dashboard_identity.name, database=storage_location.database, measurement=storage_location.measurement)

        dashboard_name = dashboard_identity.name

        # Skip dashboard creation if it already has been created while Kotori is running
        # TODO: Improve locking to prevent race conditions.
        if self.keycache.exists(*signature):
            log.debug('Data signature not changed, skip update of {whoami}', whoami=whoami)
            return

        log.info('Provisioning Grafana {whoami}', whoami=whoami)

        # Create a Grafana datasource object for designated database
        datasource_name = self.create_datasource(storage_location)

        # Try to classify designated field names from field names in message payload
        fieldnames = sorted(message.keys())
        computed_fields = BeekeeperFields(fieldnames=fieldnames).classify()

        # Create appropriate Grafana dashboard
        data_dashboard = {
            #'uid': dashboard_name + '-environment',
            'title': dashboard_identity.title,
            'datasource': datasource_name,
            'measurement_sensors': storage_location.measurement,
            'measurement_events': storage_location.measurement_events,
            'field': computed_fields,
        }

        # Debugging
        #pprint(data_dashboard)

        # Apply dashboard data to JSON template
        dashboard_json_weef = self.tpl_dashboard_weef.render(data_dashboard)

        # Get or create Grafana folder for stuffing all instant dashboards into
        folder = self.grafana_api.ensure_instant_folder()
        folder_id = folder and folder.get('id') or None

        # Create Grafana dashboards
        for dashboard_json in [dashboard_json_weef]:

            try:
                log.info('Creating/updating dashboard "{}"'.format(dashboard_name))
                response = self.grafana_api.grafana_client.dashboards.db.create(
                    folderId=folder_id, dashboard=json.loads(dashboard_json), overwrite=True)
                log.info(u'Grafana response: {response}', response=json.dumps(response))

            except GrafanaPreconditionFailedError as ex:
                message = str(ex)
                if 'name-exists' in message or 'A dashboard with the same name already exists' in message:
                    log.warn(message)
                else:
                    log.error('GrafanaPreconditionFailedError: {ex}', ex=message)

            except GrafanaClientError as ex:
                message = str(ex)
                log.error('GrafanaClientError: {ex}', ex=message)

        # Remember dashboard/panel creation for this kind of data inflow
        self.keycache.set(storage_location.database, storage_location.measurement)


@attr.s
class BeekeeperFields(object):

    fieldnames = attr.ib()

    def classify(self):

        log.debug(u'Classifying beekeeper fields {fieldnames}', fieldnames=self.fieldnames)

        # TODO: Can we account for multiple occurrences of "weightX" fields for mapping more than one scale?

        weight_synonyms = u'(weight|wght|gewicht)'
        temperature_synonyms = u'(temperature|temp|temperatur)'
        outside_synonyms = u'(outside|out|air|außen|aussen)'

        candidates = {
            'weight_total': [
                self.from_words(weight_synonyms, 'total', exclude=['stddev']),
                self.from_words(weight_synonyms, exclude=['stddev']),
            ],
            'temperature_outside': [
                self.from_words(temperature_synonyms, outside_synonyms),
                self.from_words(temperature_synonyms),
            ],
            'temperature_inside': [
                self.from_words(temperature_synonyms, 'inside'),
                self.from_words(temperature_synonyms),
            ],
        }
        #pprint(candidates)

        results = SmartBunch()
        for name, patterns in candidates.items():
            fieldname = self.find_match(patterns)
            if fieldname is not None:
                results[name] = fieldname

        log.info(u'Classified beekeeper fields "{fields}" from "{fieldnames}"', fields=results.dump(), fieldnames=self.fieldnames)

        return results

    @staticmethod
    def from_words(*words, **kwargs):
        """
        Positive and Negative Lookahead
        https://www.regular-expressions.info/lookaround.html

        Positive lookahead
        Synopsis: q(?=u)
        Example:  (?=^.*?foo.*$)(?=^.*?bar.*$)(?=^.*?green.*$)^.*$

        Negative lookahead
        Synopsis: q(?!u)
        """
        patterns = []
        for word in words:
            patterns.append(u'(?=^.*?{word}.*$)'.format(word=word))
        if 'exclude' in kwargs:
            for word in kwargs['exclude']:
                patterns.append(u'(?!^.*?{word}.*$)'.format(word=word))
        pattern = u''.join(patterns) + u'^.*$'
        return pattern

    def find_match(self, patterns):
        # TODO: Should optimize this - don't compile regex patterns on each invocation!
        for pattern in patterns:
            matcher = re.compile(pattern, re.IGNORECASE)
            for fieldname in self.fieldnames:
                if matcher.search(fieldname):
                    return fieldname


def hiveeyes_boot(settings, debug=False):

    # Service container root
    rootService = RootService(settings=settings)

    # Channel realm
    channel = Bunch(**settings.hiveeyes)

    # Main application service
    service = MqttInfluxGrafanaService(
        channel  = channel,
        graphing = [
            HiveeyesGenericGrafanaManager(settings=settings, channel=channel),
            HiveeyesBeehiveGrafanaManager(settings=settings, channel=channel),
        ],
        strategy = WanBusStrategy()
    )

    rootService.registerService(service)
    rootService.startService()
