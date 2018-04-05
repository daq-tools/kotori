# -*- coding: utf-8 -*-
# (c) 2015-2018 Andreas Motl, <andreas@getkotori.org>
from twisted.logger import Logger
from grafana_api_client import GrafanaClient, GrafanaServerError, GrafanaPreconditionFailedError, GrafanaClientError

log = Logger()


class GrafanaApi(object):
    """
    A small wrapper around ``grafana_api_client``.
    https://pypi.python.org/pypi/grafana_api_client
    """

    def __init__(self, host='localhost', port=3000, username='admin', password='admin'):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

        # A GrafanaClient instance
        self.grafana_client = None

        # The uid of the "Instant Dashboards" folder
        self.instant_folder_uid = u'instagraf'
        self.instant_folder_title = u'# Instant Dashboards'

        self.connect()

    def connect(self):
        self.grafana_client = GrafanaClient((self.username, self.password), host=self.host, port=self.port)
        try:
            self.ensure_instant_folder()
        except Exception as ex:
            log.warn('Problem creating instant folder: {ex}', ex=ex)

    def ensure_instant_folder(self):
        return self.ensure_folder(uid=self.instant_folder_uid, title=self.instant_folder_title)

    def ensure_folder(self, uid=None, title=None):

        try:
            return self.get_folder(uid=uid)

        except GrafanaClientError as ex:

            if '404' in ex.message or 'not-found' in ex.message or 'Folder not found' in ex.message:
                log.debug('Folder with uid="{uid}" not found, creating', uid=uid)
                try:
                    return self.create_folder(uid=uid, title=title)

                except Exception as ex:
                    log.warn('Problem creating folder uid="{uid}", title="{title}": {ex}', uid=uid, title=title, ex=ex)

            else:
                log.warn('Problem getting folder uid="{uid}"": {ex}', uid=uid, ex=ex)
                raise


    def create_folder(self, uid=None, title=None):
        log.info('Creating folder with uid="{uid}" and title="{title}"', uid=uid, title=title)
        data = {}
        if uid: data['uid'] = uid
        if title: data['title'] = title
        try:
            return self.grafana_client.folders.create(**data)

        except GrafanaPreconditionFailedError as ex:
            # Ignore modifications from other users while doing our own
            # TODO: Add some locking mechanisms to protect against these issues
            if 'version-mismatch' in ex.message or 'The folder has been changed by someone else' in ex.message:
                #log.warn('{message}', message=ex.message)
                pass
            else:
                raise

    def get_folder(self, uid):
        log.info('Get folder with uid="{}"'.format(uid))
        data = self.grafana_client.folders[uid].get()
        return data

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
            print response
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
                log.info('Grafana response: {response}', response=response)

            except GrafanaClientError as ex:
                if '404' in ex.message or 'Dashboard not found' in ex.message:
                    log.warn('{message}', message=ex.message)
                else:
                    raise

        try:
            log.info('Creating/updating dashboard "{}"'.format(name))
            dashboard_payload = dashboard.wrap_api()
            response = self.grafana_client.dashboards.db.create(**dashboard_payload)
            log.info('Grafana response: {response}', response=response)

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

    def get_dashboard_by_uid(self, uid):
        """
        Will return the dashboard given the dashboard unique identifier (uid).
        http://docs.grafana.org/http_api/dashboard/#get-dashboard-by-uid

        :param uid: Unique dashboard identifier (uid)
        :return:    Dashboard data structure as dictionary
        """
        return self.grafana_client.dashboards.uid[uid].get()

    def format_dashboard_name(self, name):
        return name.replace(' ', '-')

    def demo(self):
        print grafana.org()
        #    {"id":1,"name":"Main Org."}
        #client.org.replace(name="Your Org Ltd.")
        #    {"id":1,"name":"Your Org Ltd."}

    def get_dashboards(self):
        return self.grafana_client.search(type='dash-db')
