# -*- coding: utf-8 -*-
# (c) 2020-2021 Andreas Motl <andreas@getkotori.org>
import logging
from copy import deepcopy

import pytest
import pytest_twisted
from twisted.internet import threads

from test.settings.mqttkit import settings, influx_sensors, PROCESS_DELAY
from test.util import mqtt_json_sensor, sleep, idgen

logger = logging.getLogger(__name__)


@pytest_twisted.inlineCallbacks
@pytest.mark.influxdb
def test_influxdb_tags(machinery, create_influxdb, reset_influxdb):
    """
    Publish single reading in JSON format to MQTT broker.
    Proof that all special fields are stored in the
    InfluxDB database as tags.
    """

    # Define field names which are tags.
    # FIXME: Synchronize with ``kotori.daq.influx.storage.format_chunk()``.
    tag_fields_main = ['geohash', 'latitude', 'longitude']
    tag_fields_more = ['location', 'location_id', 'location_name', 'sensor_id', 'sensor_type']

    # Submit a single measurement, without timestamp.
    data = {
        'temperature': 42.84,
        'humidity': 83.1,
        'geohash': 'aa3434',
        'latitude': 42.50,
        'longitude': 52.40,
    }

    for field in tag_fields_more:
        data[field] = idgen()

    yield threads.deferToThread(mqtt_json_sensor, settings.mqtt_topic_json, data)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY)

    # Define reference payload.
    reference = deepcopy(data)
    reference['latitude'] = str(reference['latitude'])
    reference['longitude'] = str(reference['longitude'])

    # Proof that data arrived in InfluxDB.
    record = influx_sensors.get_first_record()
    del record['time']
    assert record == reference
    yield record

    # Proof that data all special fields have been converged to tags.
    resultset = influx_sensors.client.query('SHOW TAG KEYS FROM {measurement};'.format(measurement=settings.influx_measurement_sensors))
    yield resultset

    tag_names = []
    for item in resultset[settings.influx_measurement_sensors]:
        tag_names.append(item['tagKey'])

    assert set(tag_names) == set(tag_fields_main + tag_fields_more)
