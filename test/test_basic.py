# -*- coding: utf-8 -*-
# (c) 2020-2021 Andreas Motl <andreas@getkotori.org>
import logging

import pytest
import pytest_twisted

from test.settings.basic import settings, influx_sensors, grafana, create_influxdb, reset_influxdb, reset_grafana, PROCESS_DELAY
from test.util import mqtt_json_sensor, sleep

logger = logging.getLogger(__name__)


@pytest_twisted.inlineCallbacks
@pytest.mark.mqtt
@pytest.mark.grafana
def test_mqtt_strategy_lan(machinery, create_influxdb, reset_influxdb, reset_grafana):
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
    yield sleep(PROCESS_DELAY)
    yield sleep(PROCESS_DELAY)
    yield sleep(PROCESS_DELAY)

    # Proof that data arrived in InfluxDB.
    record = influx_sensors.get_first_record()
    del record['time']
    assert record == {u'humidity': 83.1, u'temperature': 42.84}
    yield record

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
    assert target['measurement'] == settings.influx_measurement_sensors
    assert 'temperature' in target['query'] or 'humidity' in target['query']
