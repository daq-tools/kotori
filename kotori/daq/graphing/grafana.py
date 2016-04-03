# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import os
import json
from pprint import pprint
from jinja2 import Template
from pkg_resources import resource_filename
from twisted.logger import Logger
from grafana_api_client import GrafanaClient, GrafanaServerError, GrafanaPreconditionFailedError, GrafanaClientError
from kotori.util import slm

logger = Logger()

class GrafanaApi(object):

    def __init__(self, host='locahost', port=3000, username='admin', password='secret'):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

        self.grafana = None

        self.connect()

    def connect(self):
        self.grafana = GrafanaClient((self.username, self.password), host=self.host, port=self.port)

    def create_datasource(self, name=None, data=None):
        data = data or {}
        data.setdefault('name', name)
        data.setdefault('access', 'proxy')

        name = data['name']

        # TODO: can delete by datasource "id" only. have to inquire using "GET /api/datasources" first
        """
        try:
            logger.info('deleting datasource: {}'.format(name))
            response = self.grafana.datasources[name].delete()
            logger.info(slm(response))
        except GrafanaClientError as ex:
            if '404' in ex.message or 'Dashboard not found' in ex.message:
                logger.warn(slm(ex.message))
            else:
                raise
        """

        try:
            logger.info('Creating datasource "{}"'.format(name))
            response = self.grafana.datasources.create(**data)
            logger.info(slm(response))
        except GrafanaServerError as ex:
            if 'Failed to add datasource' in ex.message:
                pass
            else:
                raise

        #print grafana.datasources()


    def create_dashboard(self, dashboard, name=None, delete=False):

        if not name:
            name = dashboard.get_title()

        if delete:
            try:
                logger.info('Deleting dashboard "{}"'.format(name))
                response = self.grafana.dashboards.db[name].delete()
                logger.info(slm(response))

            except GrafanaClientError as ex:
                if '404' in ex.message or 'Dashboard not found' in ex.message:
                    logger.warn(slm(ex.message))
                else:
                    raise

        try:
            logger.info('Creating/updating dashboard "{}"'.format(name))
            #print 'dashboard:'
            #pprint(dashboard.dashboard)
            response = self.grafana.dashboards.db.create(**dashboard.wrap_api())
            logger.info(slm(response))

        except GrafanaPreconditionFailedError as ex:
            if 'name-exists' in ex.message or 'A dashboard with the same name already exists' in ex.message:
                logger.warn(slm(ex.message))
            else:
                raise

        try:
            logger.info('Checking dashboard "{}"'.format(name))
            dashboard = self.grafana.dashboards.db[name].get()
            #pprint(dashboard)
        except GrafanaClientError as ex:
            if '404' in ex.message or 'Dashboard not found' in ex.message:
                logger.warn(slm(ex.message))
            else:
                raise

    def get_dashboard(self, name):
        try:
            logger.info('Getting dashboard "{}"'.format(name))
            dashboard = self.grafana.dashboards.db[name].get()
            return dashboard['dashboard']
        except GrafanaClientError as ex:
            if '404' in ex.message or 'Dashboard not found' in ex.message:
                logger.warn(slm(ex.message))
            else:
                raise


    def demo(self):
        print grafana.org()
        #    {"id":1,"name":"Main Org."}
        #client.org.replace(name="Your Org Ltd.")
        #    {"id":1,"name":"Your Org Ltd."}


class GrafanaDashboard(object):

    def __init__(self, datasource='default', title='default', dashboard=None):

        self.datasource = datasource
        self.dashboard_title = title

        self.dashboard = dashboard

        # bookkeeping: which panel id to use when adding new panels
        # if a dashboard already exists, use the maximum id currently exists as new index
        self.panel_id = 0
        if dashboard:
            # TODO: this is hardcoded on row=0
            panels = dashboard['rows'][0]['panels']
            panel_ids = [panel['id'] for panel in panels]
            if panel_ids:
                self.panel_id = max(panel_ids)

        self.tpl_dashboard = self.get_template('grafana-dashboard.json')
        self.tpl_panel = self.get_template('grafana-panel.json')
        self.tpl_target = self.get_template('grafana-target.json')

    def build(self, measurement, row_title='default', panel_title_suffix='', panels=None):

        panels = panels or []

        data_dashboard = {
            'id': 'null',
            'title': self.dashboard_title,
            'row_title': row_title,
            'row_height': '300px',
        }

        # build panels list
        panels_json = []
        for panel in panels:
            panel_json = json.dumps(self.build_panel(measurement, panel, panel_title_suffix))
            panels_json.append(panel_json)

        dashboard_json = self.tpl_dashboard.render(data_dashboard, panels=',\n'.join(panels_json))

        self.dashboard = json.loads(dashboard_json)
        #pprint(self.dashboard)
        #raise SystemExit

        return self.dashboard

    def build_panel(self, measurement, panel, title_suffix=None):

        self.panel_id += 1

        panel_title = panel['title']
        if title_suffix:
            panel_title += ' @ ' + title_suffix

        data_panel = {
            'id': self.panel_id,
            'datasource': self.datasource,
            'panel_title': panel_title,
            'left_log_base': panel.get('scale', 1),
            'label_y': panel.get('label', ''),
            'format_y': panel.get('format', 'none'),
        }

        # build targets list from fieldnames
        targets_json = []
        for fieldname in panel['fieldnames']:
            data_target = {
                'name': fieldname,
                'alias': fieldname,
                'measurement': measurement,
            }
            target_json = self.tpl_target.render(data_target)
            targets_json.append(target_json)

        panel_json = self.tpl_panel.render(data_panel, targets=',\n'.join(targets_json))
        return json.loads(panel_json)

    def get_title(self):
        return self.dashboard.get('title')

    def wrap_api(self):
        payload = {
            "dashboard": self.dashboard,
            "overwrite": False,
        }
        return payload

    @staticmethod
    def setdefaults(adict, bdict):
        for key, value in bdict.iteritems():
            adict.setdefault(key, value)

    def get_template(self, filename):
        filename = os.path.join('resources', filename)
        return Template(file(resource_filename('kotori.daq.graphing', filename)).read())


class GrafanaManager(object):

    def __init__(self, config):
        self.config = config
        if not 'port' in self.config['grafana']:
            self.config['grafana']['port'] = '3000'

        name = self.__class__.__name__
        logger.info('Starting GrafanaManager "{}". grafana={}:{}'.format(
            name,
            self.config['grafana']['host'],
            self.config['grafana']['port']))

        self.skip_cache = {}

    def _get_skip_key(self, database, series, data):
        skip_key = '-'.join([database, series, ','.join(data.keys())])
        return skip_key

    def _skip_creation(self, database, series, data):
        skip_key = self._get_skip_key(database, series, data)
        return skip_key in self.skip_cache

    def _signal_creation(self, database, series, data):
        skip_key = self._get_skip_key(database, series, data)
        self.skip_cache[skip_key] = True

    def provision(self, database, series, data, topology=None):

        topology = topology or {}
        dashboard_name = topology.get('network', database)

        if self._skip_creation(database, series, data):
            return

        logger.info('Provisioning Grafana for database "{}" and series "{}". dashboard={}'.format(database, series, dashboard_name))

        grafana = GrafanaApi(
            host = self.config['grafana']['host'],
            port = int(self.config['grafana']['port']),
            # TODO: improve multi-tenancy / per-user isolation by using distinct credentials for each user
            username = self.config['grafana']['username'],
            password = self.config['grafana']['password'],
        )
        grafana.create_datasource(database, {
            "type":     "influxdb",
            "url":      "http://{host}:{port}/".format(
                host=self.config['influxdb']['host'],
                port=int(self.config['influxdb'].get('port', '8086'))),
            "database": database,
            # TODO: improve multi-tenancy / per-user isolation by using distinct credentials for each user
            "user":     self.config['influxdb']['username'],
            "password": self.config['influxdb']['password'],
            })


        # get dashboard if already exists
        dashboard_data = grafana.get_dashboard(name=dashboard_name)

        # wrap into convenience object
        dashboard = GrafanaDashboard(datasource=database, title=dashboard_name, dashboard=dashboard_data)

        # generate panels
        panels_new = self.panel_generator(database=database, series=series, data=data, topology=topology)

        # get labels for titles
        row_title = self.row_title(database, series, topology)
        panel_title_suffix = self.panel_title_suffix(database, series, topology)

        # create whole dashboard with all panels
        if not dashboard_data:

            # build dashboard
            dashboard.build(measurement=series, row_title=row_title, panel_title_suffix=panel_title_suffix, panels=panels_new)

            # create dashboard
            grafana.create_dashboard(dashboard, name=dashboard_name)

        # update existing dashboard, only with new panels
        else:

            # compute which panels are missing
            # TODO: this is hardcoded on row=0
            panels_exists = dashboard_data['rows'][0]['panels']
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

            logger.info(u'\n' + \
                        u'Actual titles: {panels_exists_titles},\n' + \
                        u'Target panels: {panels_new},\n' + \
                        u'Target titles: {panels_new_titles}',
                panels_exists_titles=panels_exists_titles,
                panels_new=panels_new,
                panels_new_titles=panels_new_titles,
            )

            if panels_missing_titles:

                logger.info(u'Adding missing panels {panels_missing_titles}', panels_missing_titles=panels_missing_titles)

                # establish new panels
                for panel in panels_new:
                    panel_title = panel.get('title')
                    if panel_title in panels_missing_titles:
                        panels_exists.append(dashboard.build_panel(measurement=series, panel=panel, title_suffix=panel_title_suffix))

                # update dashboard with new panels
                grafana.create_dashboard(dashboard, name=dashboard_name)

            else:
                logger.info('No missing panels to add')


        # remember dashboard/panel creation for this kind of data inflow
        self._signal_creation(database, series, data)

    def row_title(self, database, series, topology):
        return database

    def panel_title_suffix(self, database, series, topology):
        return ''

    def panel_generator(self, database, series, data, topology):
        #print 'panel_generator, series: {}, data: {}'.format(series, data)

        # blacklist fields
        # _hex_ is from intercom.c
        # time is from  intercom.mqtt
        field_blacklist = ['_hex_', 'time']
        fieldnames = [key for key in data.keys() if key not in field_blacklist]

        # generate panels
        panels = []
        panels.append({'title': series,  'fieldnames': fieldnames})

        return panels

    @staticmethod
    def collect_fields(data, prefix='', sorted=True):
        """
        Field name collection helper.
        Does a prefix search over all fields in "data" and builds
        a list of field names like temp1, temp2, etc. in sorted order.
        """
        fields = []
        for field in data.keys():
            if field.startswith(prefix):
                fields.append(field)
        if sorted:
            fields.sort()
        return fields


if __name__ == '__main__':

    grafana = GrafanaApi(host='192.168.59.103', username='admin', password='secret')
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
