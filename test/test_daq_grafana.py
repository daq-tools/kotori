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
def test_mqtt_to_grafana_single(machinery, create_influxdb, reset_influxdb, reset_grafana):
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

    # Proof that Grafana is well provisioned.
    logger.info('Grafana: Checking datasource')
    assert settings.influx_database in grafana.get_datasource_names()

    logger.info('Grafana: Retrieving dashboard')
    dashboard_name = settings.grafana_dashboards[0]
    dashboard = grafana.get_dashboard_by_name(dashboard_name)

    logger.info('Grafana: Checking dashboard layout')
    target = dashboard['dashboard']['rows'][0]['panels'][0]['targets'][0]
    assert target['measurement'] == settings.influx_measurement_sensors
    assert 'temperature' in target['query'] or 'humidity' in target['query']


@pytest_twisted.inlineCallbacks
@pytest.mark.grafana
def test_mqtt_to_grafana_update_panel(machinery, create_influxdb, reset_influxdb, reset_grafana):
    """
    Publish two subsequent readings in JSON format to MQTT broker and proof
    that a corresponding datasource and a dashboard was first created and
    then updated in Grafana.
    """

    # Submit a single measurement, without timestamp.
    data = {
        'temperature': 42.84,
        'humidity': 83.1,
    }
    yield mqtt_json_sensor(settings.mqtt_topic_json, data)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY_MQTT)

    # Proof that Grafana is well provisioned.
    logger.info('Grafana: Checking datasource')
    assert settings.influx_database in grafana.get_datasource_names()

    logger.info('Grafana: Retrieving dashboard')
    dashboard_name = settings.grafana_dashboards[0]
    dashboard = grafana.get_dashboard_by_name(dashboard_name)

    logger.info('Grafana: Checking measurement of first target')
    target = dashboard['dashboard']['rows'][0]['panels'][0]['targets'][0]
    assert target['measurement'] == settings.influx_measurement_sensors

    logger.info('Grafana: Checking panel fields after creation')
    assert grafana.get_field_names(dashboard_name=dashboard_name, panel_index=0) == ["humidity", "temperature"]

    # Submit another measurement, without timestamp.
    data = {
        'pressure': 1024,
    }
    yield mqtt_json_sensor(settings.mqtt_topic_json, data)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY_MQTT)

    logger.info('Grafana: Checking panel fields after update')
    assert grafana.get_field_names(dashboard_name=dashboard_name, panel_index=0) == ["humidity", "pressure", "temperature"]


@pytest_twisted.inlineCallbacks
@pytest.mark.grafana
def test_mqtt_to_grafana_two_panels(machinery, create_influxdb, reset_influxdb, reset_grafana):
    """
    Publish two subsequent readings to two different topics and proof that a
    corresponding datasource and a dashboard with two panels has been created
    in Grafana.
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
    assert settings.influx_database in grafana.get_datasource_names()

    dashboard_name = settings.grafana_dashboards[0]

    logger.info('Grafana: Check number of panels after creation')
    assert len(grafana.get_panels(dashboard_name)) == 1

    # Submit measurement to another topic.
    yield mqtt_json_sensor(settings.mqtt_topic2_json, data)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY_MQTT)

    logger.info('Grafana: Check number of panels after creation')
    assert len(grafana.get_panels(dashboard_name)) == 2


@pytest_twisted.inlineCallbacks
@pytest.mark.grafana
def test_mqtt_to_grafana_two_dashboards(machinery, create_influxdb, reset_influxdb, reset_grafana):
    """
    Publish two subsequent readings to two different topics and proof that a
    corresponding datasource and two dashboards have been created in Grafana.
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
    assert settings.influx_database in grafana.get_datasource_names()

    logger.info('Grafana: Check dashboards after creation')
    titles = grafana.get_dashboard_titles()
    assert settings.grafana_dashboards[0] in titles
    assert settings.grafana_dashboards[1] not in titles

    # Submit measurement to another topic.
    yield mqtt_json_sensor(settings.mqtt_topic3_json, data)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY_MQTT)
    yield sleep(PROCESS_DELAY_MQTT)
    yield sleep(PROCESS_DELAY_MQTT)

    logger.info('Grafana: Check dashboards after update')
    titles = grafana.get_dashboard_titles()
    assert settings.grafana_dashboards[0] in titles
    assert settings.grafana_dashboards[1] in titles
