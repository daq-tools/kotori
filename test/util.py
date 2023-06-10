# -*- coding: utf-8 -*-
# (c) 2020-2023 Andreas Motl <andreas@getkotori.org>
import os
import json
import logging
import random
import string
import sys
import typing as t
from collections import OrderedDict

import pytest
import requests
from crate import client as cratedb_client
from crate.client.exceptions import ProgrammingError
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError
from pyinfluxql import Query
from grafana_api_client import GrafanaClient, GrafanaClientError
from twisted.internet import reactor
from twisted.internet.task import deferLater

import kotori
from kotori.daq.graphing.grafana.manager import GrafanaManager
from kotori.daq.model import TimeseriesDatabaseType

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

    def make_reset(self, dbtype: TimeseriesDatabaseType = TimeseriesDatabaseType.INFLUXDB1):

        if dbtype is TimeseriesDatabaseType.CRATEDB:
            database = self.settings.cratedb_database
            databases = getattr(self.settings, "cratedb_databases", [])
            dashboards = self.settings.grafana2_dashboards
        elif dbtype is TimeseriesDatabaseType.INFLUXDB1:
            database = self.settings.influx_database
            databases = getattr(self.settings, "influx_databases", [])
            dashboards = self.settings.grafana_dashboards

        @pytest.fixture(scope="function")
        def resetfun(machinery, machinery_cratedb):
            """
            Fixture to delete the Grafana datasource and dashboard.
            """

            logger.info('Grafana: Resetting artefacts')

            for datasource in self.client.datasources.get():
                datasource_name = datasource['name']
                logger.info(f"Attempt to delete datasource {datasource_name}")
                if datasource_name == database or datasource_name in databases:
                    datasource_id = datasource['id']
                    self.client.datasources[datasource_id].delete()
                    logger.info(f"Successfully deleted datasource {datasource_name}")

            for dashboard_name in dashboards:
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
            for machinery in [machinery, machinery_cratedb]:
                if machinery is None:
                    continue
                for app in machinery.applications:
                    for service in app.services:
                        for subservice in service.services:
                            if isinstance(subservice, GrafanaManager):
                                subservice.keycache.reset()

        return resetfun


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


class CrateDBWrapper:
    """
    Utilities for testing with CrateDB.

    Those helper functions are mostly used for test layer setup/teardown purposes.
    """

    def __init__(self, database, measurement):
        self.database = database
        self.measurement = measurement
        self.client = self.client_factory()
        self.create = None
        self.reset = None

    @staticmethod
    def client_factory():
        """
        Database client adapter factory.
        """
        # FIXME: Connectivity parameters are hardcoded.
        # TODO: Get configuration parameters from .ini file or from runtime application.
        return cratedb_client.connect(
            'localhost:4200',
            username="crate",
            pool_size=20,
            # TODO: Does configuring `timeout` actually work?
            timeout=2,
        )

    def get_tablename(self):
        """
        Provide table name per SensorWAN specification.
        """
        return f"{self.database}.{self.measurement}"

    def query(self):
        """
        Query CrateDB and respond with results in suitable shape.

        Make sure to synchronize data by using `REFRESH TABLE ...` before running
        the actual `SELECT` statement. This is applicable in test case scenarios.

        Response format::

            [
              {
                "time": ...,
                "tags": {"city": "berlin", "location": "balcony"},
                "fields": {"temperature": 42.42, "humidity": 84.84},
              },
              ...
            ]
        """
        logger.info('CrateDB: Querying database')
        db_table = self.get_tablename()
        self.execute(f"REFRESH TABLE {db_table};")
        result = self.execute(f"SELECT * FROM {db_table};")
        cols = result["cols"]
        rows = result["rows"]
        records = []
        for row in rows:
            # Build a merged record from `tags` and `fields`.
            item = dict(zip(cols, row))
            record = OrderedDict()
            record.update({"time": item["time"]})
            record.update(item["tags"])
            record.update(item["fields"])
            records.append(record)
        return records

    def execute(self, expression):
        """
        Actually execute the database query, using a cursor.
        """
        cursor = self.client.cursor()
        cursor.execute(expression)
        result = cursor._result
        cursor.close()
        return result

    def get_record(self, index=None):
        """
        Convenience method for getting specific records.
        """
        records = self.query()

        # Check number of records.
        assert len(records) >= 1, "No data in database: len(result) = {}".format(len(records))

        # Pick and return requested record.
        return records[index]

    def get_first_record(self):
        """
        Convenience method for getting the first record.
        """
        return self.get_record(index=0)

    def drop_table(self, tablename: str):
        """
        Drop the table on test suite teardown.
        """
        sql_ddl = f"DROP TABLE {tablename}"
        self.execute(sql_ddl)

    def make_create_db(self):
        """
        Support fixture for test suite setup: Creates the `database` entity.

        Attention: Creating a database is effectively a no-op with CrateDB, so
                   this is only here for symmetry reasons.
        """
        @pytest.fixture(scope="package")
        def create():
            # logger.info('CrateDB: Creating database')
            # self.client.drop_database(self.database)
            # self.client.create_database(self.database)
            pass
        return create

    def make_reset_measurement(self):
        """
        Support fixture for test suite setup: Make sure to start without existing tables.
        """

        @pytest.fixture(scope="function")
        def reset_measurement():
            logger.info('CrateDB: Resetting database')
            # Clear out the database table.
            try:
                self.drop_table(self.get_tablename())
            except ProgrammingError as ex:
                if "SchemaUnknownException" not in ex.message:
                    raise

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
