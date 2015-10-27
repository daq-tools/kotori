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
            logger.info('Creating dashboard "{}"'.format(name))
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

    def demo(self):
        print grafana.org()
        #    {"id":1,"name":"Main Org."}
        #client.org.replace(name="Your Org Ltd.")
        #    {"id":1,"name":"Your Org Ltd."}


class GrafanaDashboard(object):

    def __init__(self, datasource='default', title='default'):

        self.datasource = datasource
        self.dashboard_title = title

        self.dashboard = None

        self.tpl_dashboard = self.get_template('grafana-dashboard.json')
        self.tpl_panel = self.get_template('grafana-panel.json')
        self.tpl_target = self.get_template('grafana-target.json')

    def create(self, measurement, row_title='row', panels=None):

        panels = panels or []

        data_dashboard = {
            'id': 'null',
            'title': self.dashboard_title,
            'row_title': row_title,
            'row_height': '200px',
        }

        # build panels list
        panels_json = []
        index = 0
        for panel in panels:

            index += 1

            data_panel = {
                'id': index,
                'datasource': self.datasource,
                'title': panel['title'],
                'label_y': panel.get('label', ''),
                'format_y': panel.get('format', 'none'),
            }
            self.setdefaults(data_panel, data_dashboard)

            # build targets list from fieldnames
            targets_json = []
            for fieldname in panel['fieldnames']:
                data_target = {
                    'name': fieldname,
                    'alias': fieldname,
                    'measurement': measurement,
                }
                self.setdefaults(data_target, data_panel)
                target_json = self.tpl_target.render(data_target)
                targets_json.append(target_json)

            panel_json = self.tpl_panel.render(data_panel, targets=',\n'.join(targets_json))
            panels_json.append(panel_json)

        dashboard_json = self.tpl_dashboard.render(data_dashboard, panels=',\n'.join(panels_json))

        self.dashboard = json.loads(dashboard_json)
        #pprint(self.dashboard)
        #raise SystemExit

        return self.dashboard

    def get_title(self):
        return self.dashboard.get('title')

    def wrap_api(self):
        payload = {
            "dashboard": self.dashboard,
            "overwrite": False
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
        if not self.config.has_option('grafana', 'port'):
            self.config.set('grafana', 'port', '3000')

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

        if self._skip_creation(database, series, data):
            return

        grafana = GrafanaApi(
            host = self.config.get('grafana', 'host'),
            port = int(self.config.get('grafana', 'port')),
            # TODO: improve multi-tenancy / per-user isolation by using distinct credentials for each user
            username = self.config.get('grafana', 'username'),
            password = self.config.get('grafana', 'password'),
        )
        grafana.create_datasource(database, {
            "type":     "influxdb",
            "url":      "http://{host}:{port}/".format(
                host=self.config.get('influxdb', 'host'),
                port=self.config.get('influxdb', 'port')),
            "database": database,
            # TODO: improve multi-tenancy / per-user isolation by using distinct credentials for each user
            "user":     self.config.get('influxdb', 'username'),
            "password": self.config.get('influxdb', 'password'),
            })


        # generate panels
        panels = self.panel_generator(data)

        dashboard = GrafanaDashboard(datasource=database, title=database)
        row_title = 'node={node},gw={gateway}'.format(**topology)
        dashboard.create(measurement=series, row_title=row_title, panels=panels)
        grafana.create_dashboard(dashboard)

        self._signal_creation(database, series, data)

    def panel_generator(self, data):
        raise NotImplementedError()

    # field name collection helper
    @staticmethod
    def collect_fields(data, prefix=''):
        fields = []
        for field in data.keys():
            if field.startswith(prefix):
                fields.append(field)
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
