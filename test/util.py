# -*- coding: utf-8 -*-
# (c) 2020-2021 Andreas Motl <andreas@getkotori.org>
import os
import json
import logging
import random
import string
import sys

import pytest
import requests
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError
from pyinfluxql import Query
from grafana_api_client import GrafanaClient, GrafanaClientError
from twisted.internet import reactor
from twisted.internet.task import deferLater

import kotori


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

    def make_reset(self):

        @pytest.fixture(scope="function")
        def reset_grafana():
            """
            Fixture to delete the Grafana datasource and dashboard.
            """

            logger.info('Grafana: Resetting artefacts')

            for datasource in self.client.datasources.get():
                if datasource['name'] == self.settings.influx_database:
                    datasource_id = datasource['id']
                    self.client.datasources[datasource_id].delete()
                    break

            for dashboard_name in self.settings.grafana_dashboards:
                try:
                    self.client.dashboards.db[dashboard_name].delete()
                except GrafanaClientError as ex:
                    if '404' not in str(ex):
                        raise

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
        influx_client = self.get_client()
        result = influx_client.query(str(expression))
        return result

    def get_record(self, index=None):
        result = self.query()

        # One measurement?
        assert len(result) == 1

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
            influx.client.delete_series(self.database, measurement=self.measurement)
            #try:
            #except InfluxDBClientError as ex:
            #    if 'database not found: mqttkit_1_itest' not in ex.message:
            #        raise

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
            mosquitto_pub = "docker run --rm --network=host eclipse-mosquitto:1.6.12 mosquitto_pub -h localhost"
        elif sys.platform == "darwin":
            mosquitto_pub = "docker run --rm eclipse-mosquitto:1.6.12 mosquitto_pub -h host.docker.internal"
        else:
            raise NotImplementedError(f"Invoking 'mosquitto_pub' through Docker on '{sys.platform}' not supported yet")
    else:
        mosquitto_pub = "mosquitto_pub -h localhost"
    command = f"{mosquitto_pub} -t '{topic}' -m '{payload}'"

    logger.info('Running command {}'.format(command))
    exitcode = os.system(command)
    if exitcode != 0:
        raise ChildProcessError(f"Invoking command failed: {command}. Exit code: {exitcode}")


def http_json_sensor(topic, data):
    uri = 'http://localhost:24642/api{}'.format(topic)
    logger.info('HTTP: Submitting reading to {} using JSON'.format(uri))
    requests.post(uri, json=data)


def http_form_sensor(topic, data):
    uri = 'http://localhost:24642/api{}'.format(topic)
    logger.info('HTTP: Submitting reading to {} using x-www-form-urlencoded'.format(uri))
    requests.post(uri, data=data)


def http_csv_sensor(topic, data):
    uri = 'http://localhost:24642/api{}'.format(topic)
    logger.info('HTTP: Submitting reading to {} using CSV'.format(uri))
    body = ''
    body += '## {}\n'.format(','.join(map(str, list(data.keys()))))
    body += '{}\n'.format(','.join(map(str, list(data.values()))))
    requests.post(uri, data=body, headers={'Content-Type': 'text/csv'})


def http_get_data(topic=None, format='csv', ts_from=None, ts_to=None):
    uri = 'http://localhost:24642/api{topic}.{format}?from={ts_from}&to={ts_to}'.format(
        topic=topic, format=format, ts_from=ts_from, ts_to=ts_to)
    logger.info('HTTP: Exporting data from {} using format "{}"'.format(uri, format))
    payload = requests.get(uri).content
    if format in ["csv", "txt", "json", "html"]:
        payload = payload.decode()
    return payload


def idgen(size=6, chars=string.ascii_uppercase + string.digits):
    """
    ========
    Synopsis
    ========
    ```
    >>> idgen()
    'G5G74W'
    ```

    - https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits/2257449#2257449
    """
    return ''.join(random.choice(chars) for _ in range(size))
