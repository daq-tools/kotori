# -*- coding: utf-8 -*-
# (c) 2020-2021 Andreas Motl <andreas@getkotori.org>
import logging

import pytest
import pytest_twisted

from test.settings.mqttkit import settings, grafana, PROCESS_DELAY_MQTT
from test.util import mqtt_json_sensor, sleep

logger = logging.getLogger(__name__)


@pytest_twisted.inlineCallbacks
@pytest.mark.grafana
def test_mqtt_to_grafana(machinery, create_influxdb, reset_influxdb, reset_grafana):
    """
    Publish single reading in JSON format to MQTT broker and proof
    that a corresponding datasource and a dashboard was created in Grafana.
    """

    # Submit a single measurement, without timestamp.
    data = {
        'temperature': 42.84,
        'humidity': 83.1,
    }
    yield mqtt_json_sensor(settings.mqtt_topic_json, data)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY_MQTT)
    yield sleep(PROCESS_DELAY_MQTT)
    yield sleep(PROCESS_DELAY_MQTT)

    # Proof that Grafana is well provisioned.
    logger.info('Grafana: Checking datasource')
    datasource_names = []
    for datasource in grafana.client.datasources.get():
        datasource_names.append(datasource['name'])
    assert settings.influx_database in datasource_names

    logger.info('Grafana: Retrieving dashboard')
    dashboard_name = settings.grafana_dashboards[0]
    dashboard = grafana.get_dashboard_by_name(dashboard_name)

    logger.info('Grafana: Checking dashboard layout')
    target = dashboard['dashboard']['rows'][0]['panels'][0]['targets'][0]
    assert target['measurement'] == settings.influx_measurement_sensors
    assert 'temperature' in target['query'] or 'humidity' in target['query']
