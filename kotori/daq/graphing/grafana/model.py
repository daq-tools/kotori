# -*- coding: utf-8 -*-
# (c) 2015-2018 Andreas Motl, <andreas@getkotori.org>
import os
import json
from bunch import Bunch
from jinja2 import Template
from pkg_resources import resource_filename
from twisted.logger import Logger
from pyramid.settings import asbool

log = Logger()


class GrafanaDashboard(object):

    def __init__(self, channel=None, uid=None, title='default', datasource='default', folder_id=None, dashboard_data=None):
        self.channel = channel or Bunch()
        self.dashboard_uid = uid
        self.dashboard_title = title
        self.datasource = datasource
        self.folder_id = folder_id

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

        dashboard_tags = ['instant']
        if 'realm' in self.channel:
            dashboard_tags.append(self.channel.realm)

        data_dashboard = {
            'id': 'null',
            'uid': self.dashboard_uid,
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
        if self.folder_id is not None:
            payload['folderId'] = self.folder_id
        return payload

    @staticmethod
    def setdefaults(adict, bdict):
        for key, value in bdict.iteritems():
            adict.setdefault(key, value)
