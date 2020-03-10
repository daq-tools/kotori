# -*- coding: utf-8 -*-
# (c) 2020 Andreas Motl <andreas@getkotori.org>
import logging
import pytest_twisted

from test.resources import influx, mqtt_topic
from test.util import mqtt_sensor, sleep

logger = logging.getLogger(__name__)


@pytest_twisted.inlineCallbacks
def test_mqtt_to_influxdb_basic(machinery, create_influxdb, reset_influxdb):

    # Submit a single measurement, without timestamp.
    data = {
        'temperature': 42.84,
        'humidity': 83.1,
    }
    yield mqtt_sensor(mqtt_topic, data)

    # Wait for some time to process the message.
    yield sleep(0.2)

    # Check if data arrived in InfluxDB.
    record = influx.get_first_record()
    del record['time']
    assert record == {u'humidity': 83.1, u'temperature': 42.84}
    yield record
