# -*- coding: utf-8 -*-
# (c) 2020-2023 Andreas Motl <andreas@getkotori.org>
import os
import json
import logging
import random
import string
import sys
import typing as t

import pytest
import requests
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError
from pyinfluxql import Query
from grafana_api_client import GrafanaClient, GrafanaClientError
from twisted.internet import reactor
from twisted.internet.task import deferLater

import kotori
from kotori.daq.graphing.grafana.manager import GrafanaManager

logger = logging.getLogger(__name__)


def boot_kotori(config):
    options = {
        '--config': config,
        '--debug': True,
        '--debug_io': True,
        '--debug_mqtt': True,
        '--debug_influx': True,
    }
    loader = kotori.boot(options)
    return loader


class GrafanaWrapper:

    def __init__(self, settings):
        self.settings = settings
        self.client = self.get_client()

    def get_client(self):
        return GrafanaClient((self.settings.grafana_username, self.settings.grafana_password), host='localhost', port=3000)

    def get_datasource_names(self):
        names = []
        for datasource in self.client.datasources.get():
            names.append(datasource['name'])
        return names

    def get_dashboard_titles(self):
        titles = []
        for dashboard in self.client.search():
            titles.append(dashboard["title"])
        return titles

    def find_dashboard_by_name(self, name):
        dashboards = self.client.search()
        for dashboard in dashboards:
            if dashboard["title"] == name:
                dashboard_uid = dashboard["uid"]
                dashboard = self.client.dashboards.uid[dashboard_uid].get()
                return dashboard["dashboard"]
        raise KeyError(f"Unable to find dashboard '{name}'")

    def get_dashboard_by_name(self, name_or_uid):
        return self.find_dashboard_by_name(name=name_or_uid)

    def get_dashboard_by_uid(self, uid):
        try:
            dashboard = self.client.dashboards.uid[uid].get()
            return dashboard["dashboard"]
        except GrafanaClientError as ex:
            if '404' in str(ex):
                raise KeyError(f"Unable to find dashboard with uid={uid}")
            else:
                raise

    def get_panels(self, dashboard_name):
        dashboard = self.get_dashboard_by_name(dashboard_name)
        return dashboard['rows'][0]['panels']

    def get_field_names(self, dashboard_name, panel_index):
        panels = self.get_panels(dashboard_name)
        field_names = sorted(map(lambda x: x["fields"][0]["name"], panels[panel_index]['targets']))
        return field_names

    def make_reset(self):

        @pytest.fixture(scope="function")
        def reset_grafana(machinery):
            """
            Fixture to delete the Grafana datasource and dashboard.
            """

            logger.info('Grafana: Resetting artefacts')

            for datasource in self.client.datasources.get():
                datasource_name = datasource['name']
                logger.info(f"Attempt to delete datasource {datasource_name}")
                if datasource_name == self.settings.influx_database or \
                        datasource_name in getattr(self.settings, "influx_databases", []):
                    datasource_id = datasource['id']
                    self.client.datasources[datasource_id].delete()
                    logger.info(f"Successfully deleted datasource {datasource_name}")

            for dashboard_name in self.settings.grafana_dashboards:
                logger.info(f"Attempt to delete dashboard {dashboard_name}")
                try:
                    dashboard = self.get_dashboard_by_name(dashboard_name)
                    self.client.dashboards.uid[dashboard["uid"]].delete()
                    logger.info(f"Successfully deleted dashboard {dashboard_name}")
                except (GrafanaClientError, KeyError) as ex:
                    logger.warning(f"Unable to delete dashboard {dashboard_name}: {ex}")
                    if '404' not in str(ex) and not isinstance(ex, KeyError):
                        raise

            # Find all `GrafanaManager` service instances and invoke `KeyCache.reset()` on them.
            if machinery:
                for app in machinery.applications:
                    for service in app.services:
                        for subservice in service.services:
                            if isinstance(subservice, GrafanaManager):
                                subservice.keycache.reset()

        return reset_grafana


class InfluxWrapper:

    def __init__(self, database, measurement):
        self.database = database
        self.measurement = measurement
        self.client = self.get_client()
        self.create = None
        self.reset = None

    def get_client(self):
        # TODO: Get configuration parameters from .ini file or from runtime application.
        influx_client = InfluxDBClient(
            host='localhost',
            database=self.database,
            timeout=2)
        return influx_client

    def query(self):
        logger.info('InfluxDB: Querying database')
        expression = Query('*').from_(self.measurement) # .where(time__gte=time_begin, time__lte=time_end, **tags)
        result = self.client.query(str(expression))
        return result

    def get_record(self, index=None):
        result = self.query()

        # One measurement?
        assert len(result) == 1, "No data in database: len(result) = {}".format(len(result))

        # One record.
        records = list(result[self.measurement])
        assert len(records) >= 1

        # Check record.
        record = records[index]

        return record

    def get_first_record(self):
        return self.get_record(index=0)

    def make_create_db(self):
        @pytest.fixture(scope="package")
        def create():
            logger.info('InfluxDB: Creating database')
            #self.client.drop_database(self.database)
            self.client.create_database(self.database)
        return create

    def make_reset_measurement(self):

        @pytest.fixture(scope="function")
        def reset_measurement():
            logger.info('InfluxDB: Resetting database')
            # Clear out the database.
            influx = InfluxWrapper(database=self.database, measurement=self.measurement)
            try:
                influx.client.delete_series(self.database, measurement=self.measurement)
            except InfluxDBClientError as ex:
                if "database not found" not in str(ex):
                    raise

        return reset_measurement

        return reset_measurement


def sleep(secs):
    # https://gist.github.com/jhorman/891717
    return deferLater(reactor, secs, lambda: None)


def mqtt_json_sensor(topic, data):
    payload = json.dumps(data)
    return mqtt_sensor(topic, payload)


def mqtt_sensor(topic, payload):

    logger.info('MQTT: Submitting reading')

    # When running on CI (GHA), run ``mosquitto_pub`` from Docker image.
    # https://stackoverflow.com/questions/24319662
    if os.environ.get("CI"):
        if sys.platform == "linux":
            mosquitto_pub = "docker run --rm --network=host eclipse-mosquitto:1.6 mosquitto_pub -h localhost"
        elif sys.platform == "darwin":
            mosquitto_pub = "docker run --rm eclipse-mosquitto:1.6 mosquitto_pub -h host.docker.internal"
        else:
            raise NotImplementedError("Invoking 'mosquitto_pub' through Docker on '{}' not supported yet".format(sys.platform))
    else:
        mosquitto_pub = "mosquitto_pub -h localhost"
    command = "{mosquitto_pub} -t '{topic}' -m '{payload}'".format(mosquitto_pub=mosquitto_pub, topic=topic, payload=payload)

    logger.info('Running command {}'.format(command))
    exitcode = os.system(command)
    if exitcode != 0:
        raise ChildProcessError("Invoking command failed: {command}. Exit code: {exitcode}".format(command=command, exitcode=exitcode))


def http_raw(topic, headers=None, json=None, data=None):
    uri = 'http://localhost:24642/api{}'.format(topic)
    logger.info('HTTP: Submitting raw request to {}'.format(uri))
    return requests.post(uri, headers=headers, json=json, data=data)


def http_json_sensor(path: str, data, port=24642):
    path = path.lstrip("/")
    uri = f'http://localhost:{port}/api/{path}'
    logger.info('HTTP: Submitting reading to {} using JSON'.format(uri))
    return requests.post(uri, json=data)


def http_form_sensor(topic, data):
    uri = 'http://localhost:24642/api{}'.format(topic)
    logger.info('HTTP: Submitting reading to {} using x-www-form-urlencoded'.format(uri))
    return requests.post(uri, data=data)


def http_csv_sensor(topic, data):
    uri = 'http://localhost:24642/api{}'.format(topic)
    logger.info('HTTP: Submitting reading to {} using CSV'.format(uri))
    body = ''
    body += '## {}\n'.format(','.join(map(str, list(data.keys()))))
    body += '{}\n'.format(','.join(map(str, list(data.values()))))
    return requests.post(uri, data=body, headers={'Content-Type': 'text/csv'})


def http_get_data(path: str = None, format='csv', params=None, ts_from=None, ts_to=None, port=24642):
    path = path.lstrip("/")
    uri = f'http://localhost:{port}/api/{path}.{format}'
    logger.info('HTTP: Exporting data from {} using format "{}"'.format(uri, format))
    params = params or {}
    if ts_from:
        params["from"] = ts_from
    if ts_to:
        params["to"] = ts_to
    payload = requests.get(uri, params=params).content
    if format in ["csv", "txt", "json", "html"]:
        payload = payload.decode()
    return payload


def idgen(size=6, chars=string.ascii_uppercase + string.digits):
    """
    ========
    Synopsis
    ========

    >>> idgen()
    '...'

    - https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits/2257449#2257449
    """
    return ''.join(random.choice(chars) for _ in range(size))


def read_file(name: str) -> bytes:
    path = os.path.join(os.path.dirname(__file__), name)
    with open(path, mode="rb") as f:
        return f.read()


def read_jsonfile(name: str) -> t.Dict[str, t.Any]:
    return json.loads(read_file(name))
    path = os.path.join(os.path.dirname(__file__), name)
    with open(path, mode="r") as f:
        return json.load(f)
