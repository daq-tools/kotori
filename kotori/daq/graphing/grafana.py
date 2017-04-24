# -*- coding: utf-8 -*-
# (c) 2015-2017 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import os
import json
import types
from pprint import pprint
from collections import OrderedDict
from bunch import Bunch
from jinja2 import Template
from pkg_resources import resource_filename
from grafana_api_client import GrafanaClient, GrafanaServerError, GrafanaPreconditionFailedError, GrafanaClientError
from twisted.logger import Logger
from pyramid.settings import asbool

log = Logger()

class GrafanaApi(object):

    def __init__(self, host='localhost', port=3000, username='admin', password='admin'):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

        self.grafana_client = None

        self.connect()

    def connect(self):
        self.grafana_client = GrafanaClient((self.username, self.password), host=self.host, port=self.port)

    def create_datasource(self, name=None, data=None):
        data = data or {}
        data.setdefault('name', name)
        data.setdefault('access', 'proxy')

        name = data['name']

        # TODO: can delete by datasource "id" only. have to inquire using "GET /api/datasources" first
        """
        try:
            logger.info('deleting datasource: {}'.format(name))
            response = self.grafana_client.datasources[name].delete()
            logger.info(slm(response))
        except GrafanaClientError as ex:
            if '404' in ex.message or 'Dashboard not found' in ex.message:
                logger.warn(slm(ex.message))
            else:
                raise
        """

        try:
            log.info('Checking/Creating datasource "{}"'.format(name))
            response = self.grafana_client.datasources.create(**data)
            log.info('response: {response}', response=response)
        except GrafanaServerError as ex:
            if 'Failed to add datasource' in ex.message:
                pass
            else:
                raise
        except GrafanaClientError as ex:
            if 'Data source with same name already exists' in ex.message:
                pass
            else:
                raise

        #print grafana.datasources()


    def create_dashboard(self, dashboard, name=None, delete=False):

        if not name:
            name = dashboard.get_title()

        name = self.format_dashboard_name(name)

        if delete:
            try:
                log.info('Deleting dashboard "{}"'.format(name))
                response = self.grafana_client.dashboards.db[name].delete()
                log.info('response: {response}', response=response)

            except GrafanaClientError as ex:
                if '404' in ex.message or 'Dashboard not found' in ex.message:
                    log.warn('{message}', message=ex.message)
                else:
                    raise

        try:
            log.info('Creating/updating dashboard "{}"'.format(name))
            #print 'dashboard:'
            #pprint(dashboard.dashboard)
            response = self.grafana_client.dashboards.db.create(**dashboard.wrap_api())
            log.info('response: {response}', response=response)

        except GrafanaPreconditionFailedError as ex:
            if 'name-exists' in ex.message or 'A dashboard with the same name already exists' in ex.message:
                log.warn('{message}', message=ex.message)
            else:
                raise

        try:
            log.info('Checking dashboard "{}"'.format(name))
            dashboard = self.grafana_client.dashboards.db[name].get()
        except GrafanaClientError as ex:
            if '404' in ex.message or 'Dashboard not found' in ex.message:
                log.warn('{message}', message=ex.message)
            else:
                raise

    def get_dashboard(self, name):
        try:
            name = self.format_dashboard_name(name)
            log.info('Getting dashboard "{}"'.format(name))
            dashboard = self.grafana_client.dashboards.db[name].get()
            return dashboard['dashboard']
        except GrafanaClientError as ex:
            if '404' in ex.message or 'Dashboard not found' in ex.message:
                log.info('{message}', message=ex.message)
            else:
                raise

    def format_dashboard_name(self, name):
        return name.replace(' ', '-')

    def demo(self):
        print grafana.org()
        #    {"id":1,"name":"Main Org."}
        #client.org.replace(name="Your Org Ltd.")
        #    {"id":1,"name":"Your Org Ltd."}


class GrafanaDashboard(object):

    def __init__(self, channel=None, datasource='default', title='default', dashboard_data=None):
        self.channel = channel or Bunch()
        self.datasource = datasource
        self.dashboard_title = title

        self.dashboard_data = dashboard_data

        # bookkeeping: which panel id to use when adding new panels
        # if a dashboard already exists, use the maximum id currently exists as new index
        self.panel_id = 0
        if dashboard_data:

            # FIXME: This is hardcoded on row=0
            if dashboard_data['rows'][0]['panels'] == [None]:
                del dashboard_data['rows'][0]['panels'][0]

            panels = dashboard_data['rows'][0]['panels']
            panel_ids = [panel['id'] for panel in panels]
            if panel_ids:
                self.panel_id = max(panel_ids)

        self.tpl_dashboard = self.get_template('grafana-dashboard.json')
        self.tpl_annotation = self.get_template('grafana-annotation.json')
        self.tpl_panel = self.get_template('grafana-panel.json')
        self.tpl_target = self.get_template('grafana-target.json')

    def get_template(self, filename):
        filename = os.path.join('resources', filename)
        return Template(file(resource_filename('kotori.daq.graphing', filename)).read())

    def build(self, measurement, row_title='default', panels=None):

        panels = panels or []
        #pprint(dict(self.channel))

        dashboard_tags = ['automatic']
        if 'realm' in self.channel:
            dashboard_tags.append(self.channel.realm)

        data_dashboard = {
            'id': 'null',
            'title': self.dashboard_title,
            'row_title': row_title,
            'row_height': '300px',
            'tags': json.dumps(dashboard_tags),
            'datasource': self.datasource,
        }

        # build panels list
        panels_json = []
        for panel in panels:
            panel_json = json.dumps(self.build_panel(panel, measurement))
            panels_json.append(panel_json)

        dashboard_json = self.tpl_dashboard.render(data_dashboard, panels=',\n'.join(panels_json))

        self.dashboard_data = json.loads(dashboard_json)
        #pprint(self.dashboard)
        #raise SystemExit

        return self.dashboard_data

    def build_annotation(self, datasource, measurement):
        data_annotation = {
            'datasource': datasource,
            'name': self.get_annotation_name(measurement),
            'measurement': measurement,
            }
        annotation_json = self.tpl_annotation.render(data_annotation)
        return json.loads(annotation_json)

    def get_annotation_name(self, measurement):
        return 'Events {}'.format(measurement.replace('_events', ''))

    def update_annotations(self, measurement):
        annotations = self.dashboard_data.get('annotations', {}).get('list', [])
        found = False
        for annotation in annotations:
            if annotation['name'] == self.get_annotation_name(measurement):
                found = True
        if not found:
            annotations.append(self.build_annotation(self.datasource, measurement))

    def build_panel(self, panel, measurement):

        self.panel_id += 1

        try:
            legend_right_side = asbool(self.channel.settings.graphing_legend_right_side)
        except AttributeError:
            legend_right_side = False

        data_panel = {
            'id': self.panel_id,
            'datasource': self.datasource,
            'panel_title': panel.get('title', 'default'),
            'left_log_base': panel.get('scale', 1),
            'label_y': panel.get('label', ''),
            'format_y': panel.get('format', 'none'),
            'legend_right_side': json.dumps(legend_right_side),
        }

        # Build targets list from fieldnames
        targets_list = []
        for fieldname in panel['fieldnames']:
            data_target = self.get_target(panel, measurement, fieldname)
            target_json = self.build_target(data_target)
            targets_list.append(target_json)

        targets_json = ',\n'.join(targets_list)
        panel_json = self.tpl_panel.render(data_panel, targets=targets_json)
        #print 'panel_json:', panel_json
        try:
            return json.loads(panel_json)
        except Exception:
            log.failure(u'Failed building valid JSON for Grafana panel. data={data}, json={json}',
                data=data_panel, json=panel_json)

    def get_target(self, panel, measurement, fieldname):
        data_target = {
            'measurement': measurement,
            'name': fieldname,
            'alias': fieldname,
            'tags': json.dumps(self.serialize_tags(panel.get('tags', {}))),
        }
        return data_target

    def build_target(self, data_target):
        return self.tpl_target.render(data_target)

    def serialize_tags(self, tags):
        # Compute tags for WHERE constraint
        """
        "tags": [
                {
                "key": "gateway",
                "operator": "=",
                "value": "area_42"
            },
                {
                "condition": "AND",
                "key": "node",
                "operator": "=",
                "value": "node_1"
            }
        ],
        """
        tag_list = []
        for key, value in tags.iteritems():
            tag_entry = {
                "condition": "AND",
                "key": key,
                "operator": "=",
                "value": value,
            }
            tag_list.append(tag_entry)
        return tag_list

    def get_title(self):
        return self.dashboard_data.get('title')

    def wrap_api(self):
        payload = {
            "dashboard": self.dashboard_data,
            "overwrite": False,
        }
        return payload

    @staticmethod
    def setdefaults(adict, bdict):
        for key, value in bdict.iteritems():
            adict.setdefault(key, value)


class GrafanaManager(object):

    def __init__(self, settings=None, channel=None):
        self.config = settings
        self.channel = channel
        if not 'port' in self.config['grafana']:
            self.config['grafana']['port'] = '3000'

        name = self.__class__.__name__
        log.info('Starting GrafanaManager "{}". grafana={}:{}'.format(
            name,
            self.config['grafana']['host'],
            self.config['grafana']['port']))

        self.skip_cache = {}

        self.connect()

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

        topology = topology or {}
        dashboard_name = \
            topology.get('realm', 'default') + ' ' + \
            topology.get('network', storage_location.database) + ' automatic'

        if self._skip_creation(storage_location.database, storage_location.gateway, storage_location.node, data):
            return

        log.info('Provisioning Grafana for database "{}" and measurement "{}". dashboard={}'.format(
            storage_location.database, storage_location.measurement, dashboard_name))

        self.create_datasource(storage_location)

        # get dashboard if already exists
        dashboard_data = self.grafana.get_dashboard(name=dashboard_name)

        # wrap into convenience object
        dashboard = GrafanaDashboard(
            channel=self.channel,
            datasource=storage_location.database,
            title=dashboard_name,
            dashboard_data=dashboard_data)

        # generate panels
        panels_new = self.panel_generator(storage_location, data=data, topology=topology)
        #print 'panels_new:'; pprint(panels_new)

        # Create whole dashboard with all panels
        if not dashboard.dashboard_data:

            # Compute title for Dashboard row
            row_title = self.row_title(storage_location, topology)

            # Build dashboard representation
            dashboard.build(measurement=storage_location.measurement, row_title=row_title, panels=panels_new)

            dashboard.update_annotations(measurement=storage_location.measurement_events)

            # Create dashboard
            self.grafana.create_dashboard(dashboard, name=dashboard_name)

        else:

            # Update existing dashboard with new annotations
            #annotations = dashboard_data.get('annotations', {}).get('list', [])
            dashboard.update_annotations(measurement=storage_location.measurement_events)

            # Update existing dashboard with new panels
            if self.provision_new_panels(storage_location, dashboard, panels_new):

                # Update dashboard with new panels
                self.grafana.create_dashboard(dashboard, name=dashboard_name)

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
                    self.grafana.create_dashboard(dashboard, name=dashboard_name)


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
                    if field.startswith(prefix):
                        fields.append(field)
                        break

        if sorted:
            fields.sort()
        return fields


if __name__ == '__main__':

    grafana = GrafanaApi(host='192.168.59.103', username='admin', password='admin')
    grafana.create_datasource('hiveeyes_test', {
        "type":     "influxdb",
        "url":      "http://192.168.59.103:8086/",
        "database": "hiveeyes_test",
        "user":     "root",
        "password": "root",
    })

    dashboard = GrafanaDashboard(datasource='hiveeyes_test', title='hiveeyes_test')
    dashboard.create(measurement='1_2', row_title='node=2,gw=1', panels=[
        {'title': 'temp',      'fieldnames': ['temp1', 'temp2', 'temp3', 'temp4'], 'format': 'celsius'},
        {'title': 'humidity',  'fieldnames': ['hum1', 'hum2']},
        {'title': 'weight',    'fieldnames': ['wght1'], 'label': 'kg'},
    ])
    grafana.create_dashboard(dashboard)
