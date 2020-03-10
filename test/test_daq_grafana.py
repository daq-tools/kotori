# -*- coding: utf-8 -*-
# (c) 2020 Andreas Motl <andreas@getkotori.org>
import logging

import pytest
import pytest_twisted
from grafana_api_client import GrafanaClientError

from test.resources import settings, grafana, PROCESS_DELAY
from test.util import mqtt_sensor, sleep

logger = logging.getLogger(__name__)


@pytest_twisted.inlineCallbacks
def test_mqtt_to_grafana(machinery, create_influxdb, reset_influxdb, reset_grafana):
    """
    Acquire a single reading from MQTT in JSON format and
    proof it created a datasource and a dashboard in Grafana.
    """

    # Submit a single measurement, without timestamp.
    data = {
        'temperature': 42.84,
        'humidity': 83.1,
    }
    yield mqtt_sensor(settings.mqtt_topic, data)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY)
    yield sleep(PROCESS_DELAY)
    yield sleep(PROCESS_DELAY)

    # Proof that Grafana is well provisioned.
    logger.info('Grafana: Checking datasource')
    datasource_names = []
    for datasource in grafana.client.datasources.get():
        datasource_names.append(datasource['name'])
    assert settings.influx_database in datasource_names

    logger.info('Grafana: Checking dashboard')
    dashboard_name = settings.grafana_dashboards[0]
    dashboard = grafana.client.dashboards.db[dashboard_name].get()
    target = dashboard['dashboard']['rows'][0]['panels'][0]['targets'][0]
    assert target['measurement'] == settings.influx_measurement
    assert 'temperature' in target['query'] or 'humidity' in target['query']
