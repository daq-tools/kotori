# -*- coding: utf-8 -*-
# (c) 2020-2021 Andreas Motl <andreas@getkotori.org>
import logging

import pytest
import pytest_twisted
from bunch import Bunch

from test.conftest import create_machinery
from test.settings.mqttkit import PROCESS_DELAY
from test.util import mqtt_json_sensor, sleep, InfluxWrapper, GrafanaWrapper

logger = logging.getLogger(__name__)


settings = Bunch(
    influx_database='hiveeyes_itest',
    influx_measurement='site_box_sensors',
    mqtt_topic='hiveeyes/itest/site/box/data.json',
    grafana_username='admin',
    grafana_password='admin',
    grafana_dashboards=['hiveeyes-itest-site-box', 'hiveeyes-itest'],
)

influx = InfluxWrapper(database=settings.influx_database, measurement=settings.influx_measurement)
grafana = GrafanaWrapper(settings=settings)

machinery_hiveeyes = create_machinery('./etc/test/hiveeyes.ini')
create_influxdb_hiveeyes = influx.make_create_db()
reset_influxdb_hiveeyes = influx.make_reset_measurement()
reset_grafana_hiveeyes = grafana.make_reset()


@pytest_twisted.inlineCallbacks
@pytest.mark.hiveeyes
def test_mqtt_to_grafana(machinery_hiveeyes, create_influxdb_hiveeyes, reset_influxdb_hiveeyes, reset_grafana_hiveeyes):
    """
    Publish a single reading in JSON format to MQTT and proof
    - it is stored in the InfluxDB database.
    - a corresponding datasource and dashboards have been created in Grafana.
    """

    # Submit a single measurement, without timestamp.
    data = {
        'temperature': 42.84,
        'weight': 33.33,
    }
    yield mqtt_json_sensor(settings.mqtt_topic, data)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY)

    # Wait for Grafana to create its artefacts.
    yield sleep(2)

    # Proof that data arrived in InfluxDB.
    record = influx.get_first_record()
    del record['time']
    assert record == {u'temperature': 42.84, u'weight': 33.33}
    yield record

    # Proof that Grafana is well provisioned.
    logger.info('Grafana: Checking datasource')
    datasource_names = []
    for datasource in grafana.client.datasources.get():
        datasource_names.append(datasource['name'])
    assert settings.influx_database in datasource_names

    logger.info('Grafana: Checking dashboards')
    for dashboard_name in settings.grafana_dashboards:
        dashboard = grafana.client.dashboards.db[dashboard_name].get()['dashboard']
        if 'rows' in dashboard:
            umbrella = dashboard['rows'][0]
        else:
            umbrella = dashboard
        target = umbrella['panels'][0]['targets'][0]
        #assert target['measurement'] == settings.influx_measurement
        assert 'temperature' in target['query'] or 'weight' in target['query']
