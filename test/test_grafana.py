# -*- coding: utf-8 -*-
# (c) 2020 Andreas Motl <andreas@getkotori.org>
import logging

import pytest
import pytest_twisted
from grafana_api_client import GrafanaClientError

from test.resources import grafana, PROCESS_DELAY, mqtt_topic, influx_database, grafana_dashboard, influx_measurement
from test.util import mqtt_sensor, sleep

logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def reset_grafana():

    logger.info('Grafana: Resetting artefacts')

    for datasource in grafana.client.datasources.get():
        if datasource['name'] == influx_database:
            datasource_id = datasource['id']
            grafana.client.datasources[datasource_id].delete()
            break

    try:
        grafana.client.dashboards.db[grafana_dashboard].delete()
    except GrafanaClientError as ex:
        if '404' not in ex.message:
            raise


@pytest_twisted.inlineCallbacks
def test_mqtt_to_grafana(machinery, create_influxdb, reset_influxdb, reset_grafana):

    # Submit a single measurement, without timestamp.
    data = {
        'temperature': 42.84,
        'humidity': 83.1,
    }
    yield mqtt_sensor(mqtt_topic, data)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY)
    yield sleep(PROCESS_DELAY)
    yield sleep(PROCESS_DELAY)

    # Proof that Grafana is well provisioned.
    logger.info('Grafana: Checking datasource')
    datasource_names = []
    for datasource in grafana.client.datasources.get():
        datasource_names.append(datasource['name'])
    assert influx_database in datasource_names

    logger.info('Grafana: Checking dashboard')
    dashboard = grafana.client.dashboards.db[grafana_dashboard].get()
    target = dashboard['dashboard']['rows'][0]['panels'][0]['targets'][0]
    assert target['measurement'] == influx_measurement
    assert 'temperature' in target['query'] or 'humidity' in target['query']
