# -*- coding: utf-8 -*-
# (c) 2015-2021 Andreas Motl, <andreas@getkotori.org>
import os
import json

import attr
from bunch import Bunch
from jinja2 import Template
from pkg_resources import resource_filename
from twisted.logger import Logger
from pyramid.settings import asbool

log = Logger()

@attr.s
class GrafanaDashboardModel(object):
    name = attr.ib()
    title = attr.ib()
    datasource = attr.ib()
    measurement_sensors = attr.ib()
    measurement_events = attr.ib()
    uid = attr.ib(default=None)

@attr.s
class GrafanaDashboardBuilder(object):

    grafana_api = attr.ib()
    channel = attr.ib()
    topology = attr.ib()
    model = attr.ib()

    def make(self, data=None):

        dashboard_uid = self.model.uid
        dashboard_name = self.model.name
        dashboard_title = self.model.title
        datasource = self.model.datasource

        # Get or create Grafana folder for stuffing all instant dashboards into
        folder = self.grafana_api.ensure_instant_folder()
        folder_id = folder and folder.get('id') or None

        # Get dashboard if already exists
        dashboard_data = self.grafana_api.get_dashboard(name=dashboard_name)

        # Debugging
        #print 'dashboard_data:'; pprint(dashboard_data)

        # Wrap everything into convenience object
        dashboard = GrafanaDashboard(
            channel=self.channel,
            uid=dashboard_uid,
            title=dashboard_title,
            datasource=datasource,
            folder_id=folder_id,
            dashboard_data=dashboard_data)

        # Generate panels
        panels_new = self.panel_generator(data=data)
        #print 'panels_new:'; pprint(panels_new)

        # Create whole dashboard with all panels
        if not dashboard.dashboard_data:

            # Compute title for dashboard row
            row_title = self.row_title()

            # Build dashboard representation
            dashboard.build(measurement=self.model.measurement_sensors, row_title=row_title, panels=panels_new)

            # Optionally, add annotations
            dashboard.update_annotations(measurement=self.model.measurement_events)

            # Create dashboard
            self.grafana_api.create_dashboard(dashboard, name=dashboard_name)

        else:

            # Update existing dashboard with new annotations
            #annotations = dashboard_data.get('annotations', {}).get('list', [])
            dashboard.update_annotations(measurement=self.model.measurement_events)

            # Update existing dashboard with new panels
            if self.provision_new_panels(dashboard, panels_new):

                # Update dashboard with new panels
                self.grafana_api.create_dashboard(dashboard, name=dashboard_name)

            # Update existing panel with new targets
            else:
                title = self.panel_title()
                panel = self.find_panel_by_title(dashboard_data, title)
                panel_new = self.find_new_panel_by_title(panels_new, title)

                # Find existing targets (field names)
                existing_fields = []
                for target in panel.get('targets', []):
                    existing_fields.append(target.get('alias'))

                new_fields = list(set(panel_new.get('fieldnames', [])) - set(existing_fields))

                if new_fields:

                    for new_field in sorted(new_fields):
                        new_target = dashboard.get_target(panel=panel_new, measurement=self.model.measurement_sensors, fieldname=new_field)
                        new_target_json = json.loads(dashboard.build_target(new_target))
                        panel['targets'].append(new_target_json)

                    # Update dashboard with new panel targets
                    self.grafana_api.create_dashboard(dashboard, name=dashboard_name)

    def find_panel_by_title(self, dashboard, title):
        #print 'find panel by title:', title
        schema_version = dashboard.get('schemaVersion', 6)

        if schema_version >= 16:
            rows = [dashboard]
        elif schema_version >= 6:
            rows = dashboard.get('rows', [])

        for row in rows:
            for panel in row.get('panels', []):
                if panel.get('title') == title:
                    return panel
        return {}

    def find_new_panel_by_title(self, panels_new, title):
        for panel in panels_new:
            if panel.get('title') == title:
                return panel
        return {}

    def provision_new_panels(self, dashboard, panels_new):

        schema_version = dashboard.dashboard_data.get('schemaVersion', 6)

        # Compute which panels are missing
        # TODO: this is hardcoded on row=0
        if schema_version >= 16:
            panels_exists = dashboard.dashboard_data['panels']
        elif schema_version >= 6:
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
                    panels_exists.append(dashboard.build_panel(panel=panel, measurement=self.model.measurement_sensors))

            return True

        else:
            log.info('No missing panels to add')

    def row_title(self):
        if 'network' in self.topology:
            return self.topology.network
        else:
            return 'default'

    def panel_title_human(self):
        parts = []
        if 'node' in self.topology:
            parts.append('device={node}')
        if 'gateway' in self.topology:
            parts.append('site={gateway}')
        return ', '.join(parts).format(**self.topology)

    def panel_title(self, fieldname_prefixes=None):
        """
        return u'{measurement} @ {suffix}'.format(
            measurement = self.model.measurement_sensors,
            suffix = self.panel_title_suffix())
        """
        #fieldname_prefixes = fieldname_prefixes or []
        title = self.panel_title_human()
        if not title:
            title = self.model.measurement_sensors

        title_prefix = self.panel_title_prefix(fieldname_prefixes)
        if title_prefix:
            title = u'{prefix} @ {title}'.format(prefix=title_prefix, title=title)

        return title

    def panel_title_prefix(self, fieldname):
        return

    def panel_generator(self, data):
        #print 'panel_generator, measurement: {}, data: {}'.format(measurement, data)

        # Generate single panel
        panel = self.get_panel_data(data)

        return [panel]

    def get_panel_data(self, data, title=None, fieldname_prefixes=None):

        #fieldname_prefixes = fieldname_prefixes or []

        # Compute title
        if not title:
            title = self.panel_title(fieldname_prefixes)

        # Compute field names
        fieldnames = self.collect_fields(data, fieldname_prefixes)

        # Compute tags
        #tags = self.get_panel_tags()

        panel = {
            'title': title,
            'fieldnames': fieldnames,
            #'tags': tags,
        }

        panel.update(self.get_panel_options(data, fieldname_prefixes))

        return panel

    def get_panel_options(self, data, fieldname_prefixes):
        return {}

    """
    def get_panel_tags(self):
        tags = OrderedDict()
        if 'gateway' in storage_location:
            tags['gateway'] = storage_location.gateway
        if 'node' in storage_location:
            tags['node']    = storage_location.node
        return tags
    """

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

            elif isinstance(prefixes, list):
                for prefix in prefixes:
                    if field.startswith(prefix) or field.endswith(prefix):
                        fields.append(field)
                        break

        if sorted:
            fields.sort()
        return fields


class GrafanaDashboard(object):

    def __init__(self, channel=None, uid=None, title='default', datasource='default', folder_id=None, dashboard_data=None):
        self.channel = channel or Bunch()
        self.dashboard_uid = uid
        self.dashboard_title = title
        self.datasource = datasource
        self.folder_id = folder_id

        self.dashboard_data = dashboard_data

        # Bookkeeping: Which panel id to use when adding new panels?
        # If a dashboard already exists, use the maximum id currently exists as new index.
        self.panel_id = 0
        if dashboard_data:

            # Debugging dashboard JSON
            """
            msg = '''
            -----------------
            title: {title}
            datasource: {datasource}
            dashboard_data:
            {dashboard_data}
            '''
            log.info(msg, title=title, datasource=datasource, dashboard_data=pformat(dashboard_data))
            """

            schema_version = dashboard_data.get('schemaVersion', 6)
            if schema_version >= 16:

                # FIXME: This is hardcoded on row=0
                if dashboard_data['panels'] == [None]:
                    del dashboard_data['panels'][0]

                panels = dashboard_data['panels']
                panel_ids = [panel['id'] for panel in panels]
                if panel_ids:
                    self.panel_id = max(panel_ids)

            elif schema_version >= 6:

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
        return Template(open(resource_filename('kotori.daq.graphing.grafana', filename)).read())

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
        for key, value in tags.items():
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
        for key, value in bdict.items():
            adict.setdefault(key, value)
