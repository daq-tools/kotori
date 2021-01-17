# -*- coding: utf-8 -*-
# (c) 2020-2021 Andreas Motl <andreas@getkotori.org>
import logging
import pytest_twisted

from test.settings.mqttkit import settings, influx_sensors, PROCESS_DELAY
from test.util import mqtt_json_sensor, sleep

logger = logging.getLogger(__name__)


@pytest_twisted.inlineCallbacks
def test_timestamp_rfc3339(machinery, create_influxdb, reset_influxdb):
    """
    Publish single reading in JSON format to MQTT broker,
    using a timestamp in RFC3339 format.
    Proof that the timestamp is processed and stored correctly.
    """

    # Submit a single measurement, with timestamp.
    data = {
        'temperature': 42.84,
        'humidity': 83.1,
        'timestamp': '2020-03-10 03:38:37.937059000+01:00'
    }
    yield mqtt_json_sensor(settings.mqtt_topic_json, data)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY)

    # Proof that data arrived in InfluxDB.
    record = influx_sensors.get_first_record()
    assert record == {u'time': u'2020-03-10T02:38:37.937059Z', u'humidity': 83.1, u'temperature': 42.84}
    yield record


@pytest_twisted.inlineCallbacks
def test_timestamp_seconds(machinery, create_influxdb, reset_influxdb):
    """
    Publish single reading in JSON format to MQTT broker,
    using a timestamp as Unix Epoch in seconds.
    Proof that the timestamp is processed and stored correctly.
    """

    # Submit a single measurement, with timestamp.
    data = {
        'temperature': 42.84,
        'humidity': 83.1,
        'timestamp': 1583810982
    }
    yield mqtt_json_sensor(settings.mqtt_topic_json, data)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY)

    # Proof that data arrived in InfluxDB.
    record = influx_sensors.get_first_record()
    assert record == {u'time': u'2020-03-10T03:29:42Z', u'humidity': 83.1, u'temperature': 42.84}
    yield record


@pytest_twisted.inlineCallbacks
def test_timestamp_milliseconds(machinery, create_influxdb, reset_influxdb):
    """
    Publish single reading in JSON format to MQTT broker,
    using a timestamp as Unix Epoch in milliseconds.
    Proof that the timestamp is processed and stored correctly.
    """

    # Submit a single measurement, with timestamp.
    data = {
        'temperature': 42.84,
        'humidity': 83.1,
        'timestamp': 1583810982123
    }
    yield mqtt_json_sensor(settings.mqtt_topic_json, data)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY)

    # Proof that data arrived in InfluxDB.
    record = influx_sensors.get_first_record()
    assert record == {u'time': u'2020-03-10T03:29:42.123000Z', u'humidity': 83.1, u'temperature': 42.84}
    yield record


@pytest_twisted.inlineCallbacks
def test_timestamp_microseconds(machinery, create_influxdb, reset_influxdb):
    """
    Publish single reading in JSON format to MQTT broker,
    using a timestamp as Unix Epoch in microseconds.
    Proof that the timestamp is processed and stored correctly.
    """

    # Submit a single measurement, with timestamp.
    data = {
        'temperature': 42.84,
        'humidity': 83.1,
        'timestamp': 1583810982123456
    }
    yield mqtt_json_sensor(settings.mqtt_topic_json, data)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY)

    # Proof that data arrived in InfluxDB.
    record = influx_sensors.get_first_record()
    assert record == {u'time': u'2020-03-10T03:29:42.123456Z', u'humidity': 83.1, u'temperature': 42.84}
    yield record


@pytest_twisted.inlineCallbacks
def test_timestamp_nanoseconds(machinery, create_influxdb, reset_influxdb):
    """
    Publish single reading in JSON format to MQTT broker,
    using a timestamp as Unix Epoch in nanoseconds.
    Proof that the timestamp is processed and stored correctly.
    """

    # Submit a single measurement, with timestamp.
    data = {
        'temperature': 42.84,
        'humidity': 83.1,
        'timestamp': 1583810982123456789
    }
    yield mqtt_json_sensor(settings.mqtt_topic_json, data)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY)

    # Proof that data arrived in InfluxDB.
    record = influx_sensors.get_first_record()
    assert record == {u'time': u'2020-03-10T03:29:42.123457Z', u'humidity': 83.1, u'temperature': 42.84}
    yield record
