# -*- coding: utf-8 -*-
# (c) 2020-2021 Andreas Motl <andreas@getkotori.org>
import logging
import re

import pytest
import pytest_twisted
from twisted.internet import threads

from test.settings.mqttkit import settings, influx_sensors, PROCESS_DELAY_MQTT, device_influx_sensors
from test.util import mqtt_json_sensor, sleep, mqtt_sensor

logger = logging.getLogger(__name__)


@pytest_twisted.inlineCallbacks
@pytest.mark.mqtt
def test_mqtt_to_influxdb_json_single(machinery, create_influxdb, reset_influxdb):
    """
    Publish single reading in JSON format to MQTT broker
    and proof it is stored in the InfluxDB database.

    Addressing: Classic WAN path
    Example:    mqttkit-1/network/gateway/node
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
@pytest.mark.legacy
def test_mqtt_to_influxdb_json_legacy_topic(machinery, create_influxdb, reset_influxdb):
    """
    Publish single reading in JSON format to MQTT broker on legacy suffix
    and proof it is stored in the InfluxDB database.

    Addressing: Classic WAN path
    Example:    mqttkit-1/network/gateway/node
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

    Addressing: Classic WAN path + discrete
    Example:    mqttkit-1/network/gateway/node/data/field
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


@pytest_twisted.inlineCallbacks
@pytest.mark.mqtt
@pytest.mark.device
def test_mqtt_to_influxdb_json_wan_device(machinery, device_create_influxdb, device_reset_influxdb):
    """
    Run MQTT data acquisition with per-device addressing.

    Addressing: SensorWAN direct-device
    Example:    mqttkit-1/device/123e4567-e89b-12d3-a456-426614174000
    """

    # Submit a single measurement, without timestamp.
    data = {
        'temperature': 42.84,
        'humidity': 83.1,
    }
    yield threads.deferToThread(mqtt_json_sensor, settings.direct_mqtt_topic_device, data)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY_MQTT)

    # Proof that data arrived in InfluxDB.
    record = device_influx_sensors.get_first_record()
    del record['time']
    assert record == {u'humidity': 83.1, u'temperature': 42.84}
    yield record


@pytest_twisted.inlineCallbacks
@pytest.mark.mqtt
@pytest.mark.device
def test_mqtt_to_influxdb_json_wan_channel_success(machinery, create_influxdb, reset_influxdb):
    """
    Run MQTT data acquisition with per-device dashed-topo addressing.

    Addressing: Per-device WAN, with dashed topology decoding
    Example:    mqttkit-1/channel/network-gateway-node
    """

    # Submit a single measurement, without timestamp.
    data = {
        'temperature': 42.84,
        'humidity': 83.1,
    }
    yield threads.deferToThread(mqtt_json_sensor, settings.direct_mqtt_topic_channel, data)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY_MQTT)

    # Proof that data arrived in InfluxDB.
    record = influx_sensors.get_first_record()
    del record['time']
    assert record == {u'humidity': 83.1, u'temperature': 42.84}
    yield record


@pytest_twisted.inlineCallbacks
@pytest.mark.mqtt
@pytest.mark.device
def test_mqtt_to_influxdb_json_wan_channel_access_denied(machinery, create_influxdb, reset_influxdb):
    """
    Run MQTT data acquisition with per-device dashed-topo addressing.

    Addressing: Per-device WAN, with dashed topology decoding
    Example:    mqttkit-1/channel/network-gateway-node
    """

    # Submit a single measurement, without timestamp.
    data = {
        'temperature': 42.84,
        'humidity': 83.1,
    }
    yield threads.deferToThread(mqtt_json_sensor, settings.direct_mqtt_topic_channel_denied, data)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY_MQTT)

    # Proof that no data arrived in InfluxDB.
    with pytest.raises(AssertionError) as ex:
        influx_sensors.get_first_record()
    assert ex.match(re.escape("No data in database: len(result) = 0"))

    # FIXME: How to find `"Rejected access to SensorWAN network: another"` within log output?
