# -*- coding: utf-8 -*-
# (c) 2015-2018 Andreas Motl, <andreas@getkotori.org>
import json
import types
from collections import OrderedDict

from kotori.daq.graphing.grafana.api import GrafanaApi
from kotori.daq.graphing.grafana.model import GrafanaDashboard
from kotori.daq.graphing.grafana.service import DashboardRefreshTamingService
from kotori.daq.services import MultiServiceMixin
from twisted.application.service import MultiService
from twisted.logger import Logger

log = Logger()


class GrafanaManager(MultiService, MultiServiceMixin):

    def __init__(self, settings=None, channel=None):

        MultiService.__init__(self)

        # Make channel object from application settings configuration object
        self.setupChannel(channel=channel)

        # Shortcut to global settings
        self.config = settings

        if not 'port' in self.config['grafana']:
            self.config['grafana']['port'] = '3000'

        name = self.__class__.__name__
        log.info('Starting GrafanaManager "{}". grafana={}:{}'.format(
            name,
            self.config['grafana']['host'],
            self.config['grafana']['port']))

        self.skip_cache = {}

        # Boot further child services
        self.boot_workers()

        # Connect to Grafana API
        self.connect()

    def boot_workers(self):

        # Optionally enable dashboard refresh interval taming as yet another child service
        taming = self.channel.get('dashboard_refresh_taming')

        if taming:

            # Configuration convenience
            if taming == 'true':
                taming = 'standard'

            # Boot and register worker component
            service = DashboardRefreshTamingService(channel=self.channel, preset=taming)
            self.registerService(service)

    def _get_skip_key(self, *args):
        key_parts = []
        for arg in args:
            if isinstance(arg, types.StringTypes):
                key_parts.append(arg)
            elif isinstance(arg, types.DictionaryType):
                key_parts.append(','.join(arg.keys()))
        skip_key = '-'.join(key_parts)
        return skip_key

    def _skip_creation(self, *args):
        skip_key = self._get_skip_key(*args)
        return skip_key in self.skip_cache

    def _signal_creation(self, *args):
        skip_key = self._get_skip_key(*args)
        self.skip_cache[skip_key] = True

    def connect(self):

        # TODO: Improve multi-tenancy / per-user isolation by using distinct configuration values and credentials per ingress channel.

        self.grafana_api = GrafanaApi(
            host = self.config['grafana']['host'],
            port = int(self.config['grafana']['port']),
            username = self.config['grafana']['username'],
            password = self.config['grafana']['password'],
        )

    def create_datasource(self, storage_location):
        self.grafana_api.create_datasource(storage_location.database, {
            "type":     "influxdb",
            "url":      "http://{host}:{port}/".format(
                host=self.config['influxdb']['host'],
                port=int(self.config['influxdb'].get('port', '8086'))),
            "database": storage_location.database,
            "user":     self.config['influxdb']['username'],
            "password": self.config['influxdb']['password'],
            })

    def provision(self, storage_location, data, topology=None):

        # TODO: Get into templating, finally: Create a template variable for each InfluxDB tag
        # TODO: Also provision a WorldMap plugin

        # Compute effective topology information
        topology = topology or {}
        realm = topology.get('realm', 'default')
        network = topology.get('network', storage_location.database)

        # Derive dashboard uid and name from topology information
        dashboard_uid = realm + u'-' + network
        dashboard_name = realm + u' ' + network

        # Skip dashboard creation if it already has been created while Kotori is running
        if self._skip_creation(storage_location.database, storage_location.gateway, storage_location.node, data):
            return

        log.info('Provisioning Grafana for database "{}" and measurement "{}". dashboard="{}"'.format(
            storage_location.database, storage_location.measurement, dashboard_name))

        # Create a Grafana datasource object for designated database
        self.create_datasource(storage_location)

        # Get or create Grafana folder for stuffing all instant dashboards into
        folder = self.grafana_api.ensure_instant_folder()
        folder_id = folder and folder.get('id') or None

        # Get dashboard if already exists
        dashboard_data = self.grafana_api.get_dashboard(name=dashboard_name)

        # Wrap everything into convenience object
        dashboard = GrafanaDashboard(
            channel=self.channel,
            uid=dashboard_uid,
            title=dashboard_name,
            datasource=storage_location.database,
            folder_id=folder_id,
            dashboard_data=dashboard_data)

        # Generate panels
        panels_new = self.panel_generator(storage_location, data=data, topology=topology)
        #print 'panels_new:'; pprint(panels_new)

        # Create whole dashboard with all panels
        if not dashboard.dashboard_data:

            # Compute title for dashboard row
            row_title = self.row_title(storage_location, topology)

            # Build dashboard representation
            dashboard.build(measurement=storage_location.measurement, row_title=row_title, panels=panels_new)

            # Optionally, add annotations
            dashboard.update_annotations(measurement=storage_location.measurement_events)

            # Create dashboard
            self.grafana_api.create_dashboard(dashboard, name=dashboard_name)

        else:

            # Update existing dashboard with new annotations
            #annotations = dashboard_data.get('annotations', {}).get('list', [])
            dashboard.update_annotations(measurement=storage_location.measurement_events)

            # Update existing dashboard with new panels
            if self.provision_new_panels(storage_location, dashboard, panels_new):

                # Update dashboard with new panels
                self.grafana_api.create_dashboard(dashboard, name=dashboard_name)

            # Update existing panel with new targets
            else:
                title = self.panel_title(storage_location, topology)
                panel = self.find_panel_by_title(dashboard_data, title)
                panel_new = self.find_new_panel_by_title(panels_new, title)

                # Find existing targets (field names)
                existing_fields = []
                for target in panel.get('targets', []):
                    existing_fields.append(target.get('alias'))

                new_fields = list(set(panel_new.get('fieldnames', [])) - set(existing_fields))

                if new_fields:

                    for new_field in sorted(new_fields):
                        new_target = dashboard.get_target(panel=panel_new, measurement=storage_location.measurement, fieldname=new_field)
                        new_target_json = json.loads(dashboard.build_target(new_target))
                        panel['targets'].append(new_target_json)

                    # Update dashboard with new panel targets
                    self.grafana_api.create_dashboard(dashboard, name=dashboard_name)


        # Remember dashboard/panel creation for this kind of data inflow
        self._signal_creation(storage_location.database, storage_location.gateway, storage_location.node, data)

    def find_panel_by_title(self, dashboard, title):
        #print 'find panel by title:', title
        for row in dashboard.get('rows', []):
            for panel in row.get('panels', []):
                if panel.get('title') == title:
                    return panel
        return {}

    def find_new_panel_by_title(self, panels_new, title):
        for panel in panels_new:
            if panel.get('title') == title:
                return panel
        return {}

    def provision_new_panels(self, storage_location, dashboard, panels_new):

        # compute which panels are missing
        # TODO: this is hardcoded on row=0
        panels_exists = dashboard.dashboard_data['rows'][0]['panels']
        panels_exists_titles = [panel['title'] for panel in panels_exists]
        panels_new_titles = [panel['title'] for panel in panels_new]

        # v1 - naive
        #panels_missing_titles = set(panels_new_titles) - set(panels_exists_titles)

        # v2 - prefix search
        panels_missing_titles = []
        for new_title in panels_new_titles:
            found = False
            for existing_title in panels_exists_titles:
                exact_match = existing_title == new_title
                fuzzy_match = existing_title.startswith(new_title + ' ')
                if exact_match or fuzzy_match:
                    found = True
                    break
            if not found:
                panels_missing_titles.append(new_title)

        log.debug(u'\n' + \
                    u'Actual titles: {panels_exists_titles},\n' + \
                    u'Target panels: {panels_new},\n' + \
                    u'Target titles: {panels_new_titles}',
            panels_exists_titles=panels_exists_titles,
            panels_new=panels_new,
            panels_new_titles=panels_new_titles,
        )

        if panels_missing_titles:

            log.info(u'Adding missing panels {panels_missing_titles}', panels_missing_titles=panels_missing_titles)

            # establish new panels
            for panel in panels_new:
                panel_title = panel.get('title')
                if panel_title in panels_missing_titles:
                    panels_exists.append(dashboard.build_panel(panel=panel, measurement=storage_location.measurement))

            return True

        else:
            log.info('No missing panels to add')

    def row_title(self, storage_location, topology):
        return topology.network

    def panel_title_human(self, storage_location, topology):
        parts = []
        if 'node' in topology:
            parts.append('device={node}')
        if 'gateway' in topology:
            parts.append('site={gateway}')
        return ', '.join(parts).format(**topology)

    def panel_title(self, storage_location, topology, fieldname_prefixes=None):
        """
        return u'{measurement} @ {suffix}'.format(
            measurement = storage_location.measurement,
            suffix = self.panel_title_suffix(storage_location, topology))
        """
        #fieldname_prefixes = fieldname_prefixes or []
        title = self.panel_title_human(storage_location, topology)
        if not title:
            title = storage_location.measurement

        title_prefix = self.panel_title_prefix(fieldname_prefixes)
        if title_prefix:
            title = u'{prefix} @ {title}'.format(prefix=title_prefix, title=title)

        return title

    def panel_title_prefix(self, fieldname):
        return

    def panel_generator(self, storage_location, data, topology):
        #print 'panel_generator, measurement: {}, data: {}'.format(measurement, data)

        # Generate single panel
        panel = self.get_panel_data(storage_location, topology, data)

        return [panel]

    def get_panel_data(self, storage_location, topology, data, title=None, fieldname_prefixes=None):

        #fieldname_prefixes = fieldname_prefixes or []

        # Compute title
        if not title:
            title = self.panel_title(storage_location, topology, fieldname_prefixes)

        # Compute field names
        fieldnames = self.collect_fields(data, fieldname_prefixes)

        # Compute tags
        #tags = self.get_panel_tags(storage_location)

        panel = {
            'title': title,
            'fieldnames': fieldnames,
            #'tags': tags,
        }

        panel.update(self.get_panel_options(data, fieldname_prefixes))

        return panel

    def get_panel_options(self, data, fieldname_prefixes):
        return {}

    def get_panel_tags(self, storage_location):
        tags = OrderedDict()
        if 'gateway' in storage_location:
            tags['gateway'] = storage_location.gateway
        if 'node' in storage_location:
            tags['node']    = storage_location.node
        return tags

    @staticmethod
    def collect_fields(data, prefixes=None, sorted=True):
        """
        Field name collection helper.
        Does a prefix search over all fields in "data" and builds
        a list of field names like temp1, temp2, etc. in sorted order.
        """

        # Filter blacklist fields
        # _hex_ is from intercom.c
        # time is from  intercom.mqtt
        blacklist = ['_hex_', 'time']

        fields = []
        for field in data.keys():
            if field in blacklist:
                continue

            if prefixes is None:
                fields.append(field)

            elif isinstance(prefixes, types.ListType):
                for prefix in prefixes:
                    if field.startswith(prefix) or field.endswith(prefix):
                        fields.append(field)
                        break

        if sorted:
            fields.sort()
        return fields


if __name__ == '__main__':
    """
    Example usage of GrafanaApi and GrafanaDashboard objects.
    """

    # Bootstrap logging
    import sys
    import twisted
    twisted.python.log.startLogging(sys.stderr)

    # Connect to Grafana
    grafana = GrafanaApi(host='localhost', username='admin', password='admin')

    # Create Grafana Datasource object
    grafana.create_datasource('hiveeyes_test', {
        "type":     "influxdb",
        "url":      "http://localhost:8086/",
        "database": "hiveeyes_test",
        "user":     "root",
        "password": "root",
    })

    # Get or create Grafana folder for stuffing all instant dashboards into
    folder = grafana.ensure_instant_folder()
    folder_id = folder and folder.get('id') or None

    # Create dashboard
    dashboard = GrafanaDashboard(datasource='hiveeyes_test', title='hiveeyes_test', folder_id=folder_id)
    dashboard.build(measurement='1_2', row_title='node=2,gw=1', panels=[
        {'title': 'temp',      'fieldnames': ['temp1', 'temp2', 'temp3', 'temp4'], 'format': 'celsius'},
        {'title': 'humidity',  'fieldnames': ['hum1', 'hum2']},
        {'title': 'weight',    'fieldnames': ['wght1'], 'label': 'kg'},
    ])
    grafana.create_dashboard(dashboard)

    grafana.tame_refresh_interval()
