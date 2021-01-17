# -*- coding: utf-8 -*-
# (c) 2015-2021 Andreas Motl, <andreas@getkotori.org>
import arrow
from twisted.logger import Logger
from twisted.application.service import MultiService

from kotori.daq.services import MultiServiceMixin
from kotori.daq.graphing.grafana.api import GrafanaApi
from kotori.daq.graphing.grafana.dashboard import GrafanaDashboardBuilder, GrafanaDashboardModel
from kotori.daq.graphing.grafana.service import DashboardRefreshTamingService
from kotori.util.common import KeyCache, SmartBunch

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

    def get_dashboard_identity(self, storage_location, topology=None):

        # Compute effective topology information
        topology = topology or {}
        realm = topology.get('realm', 'default')

        if 'network' in topology:
            name = topology.network
        else:
            name = topology.node

        # Derive dashboard uid and name from topology information
        identity = SmartBunch(
            #uid=u'{realm}-{name}-instant'.format(realm=realm, name=name),
            name=u'{realm}-{name}'.format(realm=realm, name=name),
            title=u'{realm}-{name}'.format(realm=realm, name=name),
            # TODO: Use real title after fully upgrading to new Grafana API (i.e. don't use get-by-slug anymore!)
            #title=u'Raw data for realm={realm} network={network}'.format(realm=realm, network=network),
        )
        #print identity.prettify()

        return identity

    def provision(self, storage_location, data, topology=None):

        # TODO: Get into templating, finally: Create a template variable for each InfluxDB tag
        # TODO: Also provision a WorldMap plugin

        # The identity information of this provisioning process
        dashboard_identity = self.get_dashboard_identity(storage_location, topology)

        signature = [storage_location.database]
        if 'gateway' in storage_location:
            signature += storage_location.gateway
        signature += [storage_location.node, data]

        whoami = u'dashboard "{dashboard_name}" for database "{database}" and measurement "{measurement}"'.format(
            dashboard_name=dashboard_identity.name, database=storage_location.database, measurement=storage_location.measurement)

        # Skip dashboard creation if it already has been created while Kotori is running
        # TODO: Improve locking to prevent race conditions.
        if self.keycache.exists(*signature):
            log.debug(u'Data signature not changed, skip update of {whoami}', whoami=whoami)
            return

        log.info(u'Provisioning Grafana {whoami}', whoami=whoami)

        # Create a Grafana datasource object for designated database
        datasource_name = self.create_datasource(storage_location)

        # Define Grafana dashboard model
        model = GrafanaDashboardModel(
            #uid=dashboard_identity.uid,
            name=dashboard_identity.name,
            title=dashboard_identity.title,
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

    def tame_refresh_interval(self, preset='standard', force=False):
        """
        Tame refresh interval for all dashboards.

        :param mode: Which taming preset to use. Currently, only "standard" is
                     implemented, which is also the default preset.

        Introduction
        ------------
        The default dashboard refresh interval of 5 seconds is important
        for instant-on workbench operations. However, the update interval
        is usually just about 5 minutes after the sensor node is in the field.

        Problem
        -------
        Having high refresh rates on many dashboards can increase the overall
        system usage significantly, depending on how many users are displaying
        them in their browsers and the complexity of the database queries
        issued when rendering the dashboard.

        Solution
        --------
        In order to reduce the overall load on the data acquisition system,
        the refresh interval of dashboards not updated since a configurable
        threshold time is decreased according to rules of built-in presets.

        The default "standard" preset currently implements the following rules:

        - Leave all dashboards completely untouched which have been updated during the last 14 days
        - Apply a refresh interval of 5 minutes for all dashboards having the "live" tag
        - Completely disable refreshing for all dashboards having the "historical" tag
        - Apply a refresh interval of 30 minutes for all other dashboards

        """

        dashboard_list = self.grafana_api.get_dashboards()

        log.info('Taming dashboard refresh interval with preset="{preset}" for {count} dashboards',
                 preset=preset, count=len(dashboard_list))

        # Date of 14 days in the past
        before_14_days = arrow.utcnow().shift(days=-14)

        for dashboard_meta in dashboard_list:

            dashboard_meta = SmartBunch.bunchify(dashboard_meta)
            #print dashboard_meta.prettify()

            whoami = u'title="{title}", uid="{uid}"'.format(title=dashboard_meta['title'], uid=dashboard_meta['uid'])

            # Request dashboard by uid
            dashboard_uid = dashboard_meta['uid']
            response = self.grafana_api.get_dashboard_by_uid(dashboard_uid)
            response = SmartBunch.bunchify(response)

            # Get effective dashboard information from response
            folder_id = response.meta.folderId
            dashboard = response.dashboard

            # Compute new dashboard refresh interval by applying taming rules
            # Units: Mwdhmsy

            # 1. Check dashboard modification time against threshold
            modification_time = arrow.get(response.meta.updated)
            if not force and modification_time > before_14_days:
                log.debug('Skip taming dashboard with {whoami}, it has recently been modified', whoami=whoami)
                continue

            # 2. Apply refresh interval by looking at the dashboard tags
            if 'live' in dashboard_meta.tags:
                refresh_interval = '5m'
            elif 'historical' in dashboard_meta.tags:
                refresh_interval = None
            else:
                refresh_interval = '30m'

            # Skip update procedure if refresh interval hasn't changed at all
            if refresh_interval == dashboard.refresh:
                continue

            # Set new refresh interval
            dashboard.refresh = refresh_interval

            # Update dashboard
            log.debug('Taming dashboard with {whoami} to refresh interval of {interval}', whoami=whoami, interval=refresh_interval)
            response = self.grafana_api.grafana_client.dashboards.db.create(dashboard=dashboard, folderId=folder_id)

            # Report about the outcome
            if response['status'] == 'success':
                log.info('Successfully tamed dashboard with {whoami}', whoami=whoami)
            else:
                log.warn('Failed taming dashboard with {whoami}', whoami=whoami)


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
    manager = GrafanaManager(
        settings={"grafana": dict(host='localhost', username='admin', password='admin')},
        channel={}
    )
    grafana = manager.grafana_api

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
    manager.tame_refresh_interval()
