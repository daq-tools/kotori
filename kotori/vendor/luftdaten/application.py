# -*- coding: utf-8 -*-
# (c) 2017 Andreas Motl <andreas@getkotori.org>
import json

from pkg_resources import resource_filename
from jinja2 import Template
from twisted.logger import Logger
from grafana_api_client import GrafanaPreconditionFailedError, GrafanaClientError
from kotori.daq.services.mig import MqttInfluxGrafanaService
from kotori.daq.graphing.grafana.manager import GrafanaManager
from kotori.daq.storage.influx import InfluxDBAdapter

log = Logger()

class LuftdatenGrafanaManager(GrafanaManager):

    def __init__(self, *args, **kwargs):
        GrafanaManager.__init__(self, *args, **kwargs)
        self.tpl_dashboard_map      = self.get_template('grafana-map.json')
        self.tpl_dashboard_location = self.get_template('grafana-by-location.json')

    def get_template(self, filename):
        return Template(open(resource_filename('kotori.vendor.luftdaten', filename)).read().decode('utf-8'))

    def provision(self, storage_location, message, topology):

        topology = topology or {}
        dashboard_name = self.strategy.topology_to_label(topology)

        # The identity information of this provisioning process
        signature = (storage_location.database, storage_location.measurement)
        whoami = 'dashboard "{dashboard_name}" for database "{database}" and measurement "{measurement}"'.format(
            dashboard_name=dashboard_name, database=storage_location.database, measurement=storage_location.measurement)

        # Skip dashboard creation if it already has been created while Kotori is running
        # TODO: Improve locking to prevent race conditions.
        if self.keycache.exists(*signature):
            log.debug('Data signature not changed, skip update of {whoami}', whoami=whoami)
            return

        log.info('Provisioning Grafana {whoami}', whoami=whoami)

        # Create a Grafana datasource object for designated database
        self.create_datasource(storage_location)


        # Create appropriate Grafana dashboard

        data_dashboard = {
            'database': storage_location.database,
            'measurement': storage_location.measurement,
            'measurement_events': storage_location.measurement_events,
        }
        dashboard_json_map      = self.tpl_dashboard_map.render(data_dashboard, title='{name} map'.format(name=dashboard_name))
        dashboard_json_location = self.tpl_dashboard_location.render(data_dashboard, title='{name} by-location'.format(name=dashboard_name))

        # Get or create Grafana folder for stuffing all instant dashboards into
        folder = self.grafana_api.ensure_instant_folder()
        folder_id = folder and folder.get('id') or None

        for dashboard_json in [dashboard_json_map, dashboard_json_location]:

            try:
                log.info('Creating/updating dashboard "{}"'.format(dashboard_name))
                response = self.grafana_api.grafana_client.dashboards.db.create(
                    folderId=folder_id, dashboard=json.loads(dashboard_json), overwrite=True)
                log.info(u'Grafana response: {response}', response=json.dumps(response))

            except GrafanaPreconditionFailedError as ex:
                if 'name-exists' in ex.message or 'A dashboard with the same name already exists' in ex.message:
                    log.warn(ex.message)
                else:
                    log.error('Grafana Error: {ex}', ex=ex.message)

            except GrafanaClientError as ex:
                log.error('Grafana Error: {ex}', ex=ex.message)

        # Remember dashboard/panel creation for this kind of data inflow
        self.keycache.set(storage_location.database, storage_location.measurement)


class LuftdatenMqttInfluxGrafanaService(MqttInfluxGrafanaService):

    def setupService(self):
        MqttInfluxGrafanaService.setupService(self)
        self.settings.influxdb.use_udp = True
        self.settings.influxdb.udp_port = 4445
        self.influx = InfluxDBAdapter(settings = self.settings.influxdb)
