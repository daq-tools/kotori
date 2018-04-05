# -*- coding: utf-8 -*-
# (c) 2015-2018 Andreas Motl, <andreas@getkotori.org>
from twisted.logger import Logger
from twisted.application.service import MultiService

from kotori.daq.services import MultiServiceMixin
from kotori.daq.graphing.grafana.api import GrafanaApi
from kotori.daq.graphing.grafana.dashboard import GrafanaDashboardBuilder, GrafanaDashboardModel
from kotori.daq.graphing.grafana.service import DashboardRefreshTamingService
from kotori.util.common import KeyCache

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

        # Initialize key cache
        # Utility functions for remembering whether the dashboard has been created already.
        # This is important as we would otherwise talk to Grafana for each ingress measurement (on each hit).
        self.keycache = KeyCache()

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

    def connect(self):

        # TODO: Improve multi-tenancy / per-user isolation by using distinct configuration values and credentials per ingress channel.

        self.grafana_api = GrafanaApi(
            host = self.config['grafana']['host'],
            port = int(self.config['grafana']['port']),
            username = self.config['grafana']['username'],
            password = self.config['grafana']['password'],
        )

    def create_datasource(self, storage_location):

        datasource_name = storage_location.database

        self.grafana_api.create_datasource(datasource_name, {
            "type":     "influxdb",
            "url":      "http://{host}:{port}/".format(
                host=self.config['influxdb']['host'],
                port=int(self.config['influxdb'].get('port', '8086'))),
            "database": storage_location.database,
            "user":     self.config['influxdb']['username'],
            "password": self.config['influxdb']['password'],
            })

        return datasource_name

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

        # The identity information of this provisioning process
        signature = (storage_location.database, storage_location.gateway, storage_location.node, data)
        whoami = 'dashboard "{}" for database "{}" and measurement "{}"'.format(
            storage_location.database, storage_location.measurement, dashboard_name)

        # Skip dashboard creation if it already has been created while Kotori is running
        # TODO: Improve locking to prevent race conditions.
        if self.keycache.exists(*signature):
            log.debug('Data signature not changed, skip update of {whoami}', whoami=whoami)
            return

        log.info('Provisioning Grafana {whoami}', whoami=whoami)

        # Create a Grafana datasource object for designated database
        datasource_name = self.create_datasource(storage_location)

        # Define Grafana dashboard model
        model = GrafanaDashboardModel(
            uid=dashboard_uid,
            name=dashboard_name,
            datasource=datasource_name,
            measurement_sensors=storage_location.measurement,
            measurement_events=storage_location.measurement_events
        )

        # Create appropriate Grafana dashboard
        dashboard_builder = GrafanaDashboardBuilder(
            grafana_api=self.grafana_api,
            channel=self.channel,
            topology=topology,
            model=model
        )
        dashboard_builder.make(data=data)

        # Remember dashboard/panel creation for this kind of data inflow
        self.keycache.set(*signature)


if __name__ == '__main__':
    """
    Example usage of GrafanaApi and GrafanaDashboard objects.
    """

    # Bootstrap logging
    import sys
    import twisted
    from kotori.daq.graphing.grafana.dashboard import GrafanaDashboard

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

    # Run one-shot task to tame the dashboard intervals
    grafana.tame_refresh_interval()
