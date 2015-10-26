# -*- coding: utf-8 -*-
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
import os
import json
from pprint import pprint
from jinja2 import Template
from pkg_resources import resource_filename
from grafana_api_client import GrafanaClient, GrafanaServerError, GrafanaPreconditionFailedError, GrafanaClientError


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

    def create_datasource(self):
        try:
            print 'creating datasource'
            print self.grafana.datasources.create(**{
                "name":     "hiveeyes_test",
                "type":     "influxdb",
                "url":      "http://192.168.59.103:8086/",
                "access":   "proxy",
                "database": "hiveeyes_test",
                "user":     "admin",
                "password": "Armoojwi",
            })
        except GrafanaServerError as ex:
            if 'Failed to add datasource' in ex.message:
                pass
            else:
                raise

        #print grafana.datasources()


    def create_dashboard(self, dashboard, name=None):

        if not name:
            name = dashboard.get_title()

        try:
            print 'deleting dashboard'
            print self.grafana.dashboards.db[name].delete()

        except GrafanaClientError as ex:
            if '404' in ex.message or 'Dashboard not found' in ex.message:
                print ex.message
            else:
                raise

        try:
            print 'creating dashboard'
            print self.grafana.dashboards.db.create(**dashboard.wrap_api())

        except GrafanaPreconditionFailedError as ex:
            if 'name-exists' in ex.message or 'A dashboard with the same name already exists' in ex.message:
                print ex.message
            else:
                raise

        try:
            print 'checking dashboard'
            dashboard = self.grafana.dashboards.db[name].get()
            #pprint(dashboard)
        except GrafanaClientError as ex:
            if '404' in ex.message or 'Dashboard not found' in ex.message:
                print ex.message
            else:
                raise

    def demo(self):
        print grafana.org()
        #    {"id":1,"name":"Main Org."}
        #client.org.replace(name="Your Org Ltd.")
        #    {"id":1,"name":"Your Org Ltd."}


class GrafanaDashboard(object):

    def __init__(self, datasource, title):

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
            'datasource': self.datasource,
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


if __name__ == '__main__':
    grafana = GrafanaApi(host='192.168.59.103')
    dashboard = GrafanaDashboard('hiveeyes_test', 'hiveeyes_test')
    dashboard.create(measurement='1_2', row_title='node=2,gw=1', panels=[
        {'title': 'temp',      'fieldnames': ['temp1', 'temp2', 'temp3'], 'format': 'celsius'},
        {'title': 'humidity',  'fieldnames': ['hum1', 'hum2']},
        {'title': 'weight',    'fieldnames': ['wght1'], 'label': 'kg'},
    ])
    grafana.create_dashboard(dashboard)
