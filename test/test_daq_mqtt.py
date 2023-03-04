# -*- coding: utf-8 -*-
# (c) 2020-2021 Andreas Motl <andreas@getkotori.org>
import logging

import pytest
import pytest_twisted
from twisted.internet import threads

from test.settings.mqttkit import settings, influx_sensors, PROCESS_DELAY_MQTT
from test.util import mqtt_json_sensor, sleep, mqtt_sensor

logger = logging.getLogger(__name__)


@pytest_twisted.inlineCallbacks
@pytest.mark.mqtt
def test_mqtt_to_influxdb_json_single(machinery, create_influxdb, reset_influxdb):
    """
    Publish single reading in JSON format to MQTT broker
    and proof it is stored in the InfluxDB database.
    """

    # Submit a single measurement, without timestamp.
    data = {
        'temperature': 42.84,
        'humidity': 83.1,
    }
    yield threads.deferToThread(mqtt_json_sensor, settings.mqtt_topic_json, data)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY_MQTT)

    # Proof that data arrived in InfluxDB.
    record = influx_sensors.get_first_record()
    del record['time']
    assert record == {u'humidity': 83.1, u'temperature': 42.84}
    yield record


@pytest_twisted.inlineCallbacks
@pytest.mark.mqtt
def test_mqtt_to_influxdb_json_bulk(machinery, create_influxdb, reset_influxdb):
    """
    Publish multiple readings in JSON format to MQTT broker
    and proof it is stored in the InfluxDB database.
    """

    # Submit multiple measurements, without timestamp.
    data = [
        {
            'temperature': 21.42,
            'humidity': 41.55,
        },
        {
            'temperature': 42.84,
            'humidity': 83.1,
        },
    ]
    yield threads.deferToThread(mqtt_json_sensor, settings.mqtt_topic_json, data)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY_MQTT)

    # Proof that data arrived in InfluxDB.
    record = influx_sensors.get_record(index=0)
    del record['time']
    assert record == {u'temperature': 21.42, u'humidity': 41.55}

    record = influx_sensors.get_record(index=1)
    del record['time']
    assert record == {u'temperature': 42.84, u'humidity': 83.1}


@pytest_twisted.inlineCallbacks
@pytest.mark.mqtt
def test_mqtt_to_influxdb_json_compact_bulk(machinery, create_influxdb, reset_influxdb):
    """
    Publish multiple readings in compact JSON format to MQTT broker
    and proof they are stored in the InfluxDB database.

    https://github.com/daq-tools/kotori/issues/39
    """

    # Submit multiple measurements, with timestamp.
    data = {
        "1611082554": {
            "temperature": 21.42,
            "humidity": 41.55,
        },
        "1611082568": {
            "temperature": 42.84,
            "humidity": 83.1,
        },
    }
    yield threads.deferToThread(mqtt_json_sensor, settings.mqtt_topic_json_compact, data)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY_MQTT)

    # Proof that data arrived in InfluxDB.
    record = influx_sensors.get_record(index=0)
    assert record == {u'time': '2021-01-19T18:55:54Z', u'temperature': 21.42, u'humidity': 41.55}

    record = influx_sensors.get_record(index=1)
    assert record == {u'time': '2021-01-19T18:56:08Z', u'temperature': 42.84, u'humidity': 83.1}


@pytest_twisted.inlineCallbacks
@pytest.mark.mqtt
@pytest.mark.legacy
def test_mqtt_to_influxdb_json_legacy_topic(machinery, create_influxdb, reset_influxdb):
    """
    Publish single reading in JSON format to MQTT broker on legacy suffix
    and proof it is stored in the InfluxDB database.
    """

    # Submit a single measurement, without timestamp.
    data = {
        'temperature': 42.84,
        'humidity': 83.1,
    }
    yield threads.deferToThread(mqtt_json_sensor, settings.mqtt_topic_json_legacy, data)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY_MQTT)

    # Proof that data arrived in InfluxDB.
    record = influx_sensors.get_first_record()
    assert 'temperature' in record or 'humidity' in record


@pytest_twisted.inlineCallbacks
@pytest.mark.mqtt
def test_mqtt_to_influxdb_discrete(machinery, create_influxdb, reset_influxdb):
    """
    Publish discrete values to the MQTT broker
    and proof they are stored in the InfluxDB database.
    """

    # Submit discrete measurement values, without timestamp.
    topic_temperature = settings.mqtt_topic_single + '/temperature'
    topic_humidity = settings.mqtt_topic_single + '/humidity'
    yield threads.deferToThread(mqtt_sensor, topic_temperature, 42.84)
    yield threads.deferToThread(mqtt_sensor, topic_humidity, 83.1)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY_MQTT)

    # Proof that data arrived in InfluxDB.
    record = influx_sensors.get_first_record()
    assert 'temperature' in record or 'humidity' in record
