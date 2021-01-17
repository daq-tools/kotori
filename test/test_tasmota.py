# -*- coding: utf-8 -*-
# (c) 2020-2021 Andreas Motl <andreas@getkotori.org>
import json
import logging

import pytest
import pytest_twisted

from test.settings.mqttkit import influx_sensors, PROCESS_DELAY
from test.util import mqtt_json_sensor, sleep

logger = logging.getLogger(__name__)


tasmota_sensor_topic = 'mqttkit-1/itest/foo/bar/tele/SENSOR'
tasmota_state_topic = 'mqttkit-1/itest/foo/bar/tele/STATE'


@pytest_twisted.inlineCallbacks
@pytest.mark.tasmota
def test_tasmota_sonoff_sc(machinery, create_influxdb, reset_influxdb):
    """
    Publish a single SENSOR reading in Tasmota/JSON format
    to MQTT broker, including a timestamp.
    Proof that the reading is processed and stored correctly.

    https://getkotori.org/docs/handbook/decoders/tasmota.html#submit-example-payload
    """

    # Submit a single measurement.
    data = {
      "Time": "2019-06-02T22:13:07",
      "SonoffSC": {
        "Temperature": 25,
        "Humidity": 15,
        "Light": 20,
        "Noise": 10,
        "AirQuality": 90
      },
      "TempUnit": "C"
    }
    yield mqtt_json_sensor(tasmota_sensor_topic, data)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY)

    # Define reference data.
    reference = {
      u'time': u'2019-06-02T20:13:07Z',
      u'SonoffSC.AirQuality': 90,
      u'SonoffSC.Humidity': 15,
      u'SonoffSC.Light': 20,
      u'SonoffSC.Noise': 10,
      u'SonoffSC.Temperature': 25,
    }

    # Proof that data arrived in InfluxDB.
    record = influx_sensors.get_first_record()
    assert record == reference
    yield record


@pytest_twisted.inlineCallbacks
@pytest.mark.tasmota
def test_tasmota_ds18b20(machinery, create_influxdb, reset_influxdb):
    """
    Publish another single SENSOR reading in Tasmota/JSON format
    to MQTT broker, including a timestamp.
    Proof that the reading is processed and stored correctly.

    https://getkotori.org/docs/handbook/decoders/tasmota.html#submit-example-payload
    """

    # Submit a single measurement.
    data = {
      "Time": "2017-02-16T10:13:52",
      "DS18B20": {
        "Temperature": 20.6
      }
    }
    yield mqtt_json_sensor(tasmota_sensor_topic, data)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY)

    # Define reference data.
    reference = {
      u'time': u'2017-02-16T09:13:52Z',
      u'DS18B20.Temperature': 20.6,
    }

    # Proof that data arrived in InfluxDB.
    record = influx_sensors.get_first_record()
    assert record == reference
    yield record


@pytest_twisted.inlineCallbacks
@pytest.mark.tasmota
@pytest.mark.wemos
def test_tasmota_wemos_dht22(machinery, create_influxdb, reset_influxdb):
    """
    Publish a reading from a Wemos multi sensor device.
    Proof that the reading is processed and stored correctly.
    """

    # Submit a single measurement.
    data = {
      "Time": "2017-10-05T22:39:55",
      "DHT22": {
        "Temperature": 25.4,
        "Humidity": 45
      },
      "TempUnit": "C"
    }
    yield mqtt_json_sensor(tasmota_sensor_topic, data)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY)

    # Define reference data.
    reference = {
        u'time': u'2017-10-05T20:39:55Z',
        u'DHT22.Temperature': 25.4,
        u'DHT22.Humidity': 45,
    }

    # Proof that data arrived in InfluxDB.
    record = influx_sensors.get_first_record()
    assert record == reference
    yield record


@pytest_twisted.inlineCallbacks
@pytest.mark.tasmota
@pytest.mark.wemos
def test_tasmota_wemos_multi(machinery, create_influxdb, reset_influxdb):
    """
    Publish a reading from a Wemos multi sensor device.
    Proof that the reading is processed and stored correctly.
    """

    # Submit a single measurement.
    data = {
      "Time": "2017-10-05T22:39:45",
      "DS18x20": {
        "DS1": {
          "Type": "DS18B20",
          "Address": "28FF4CBFA41604C4",
          "Temperature": 25.37
        },
        "DS2": {
          "Type": "DS18B20",
          "Address": "28FF1E7FA116035D",
          "Temperature": 30.44
        },
        "DS3": {
          "Type": "DS18B20",
          "Address": "28FF1597A41604CE",
          "Temperature": 25.81
        }
      },
      "DHT22": {
        "Temperature": 33.2,
        "Humidity": 30
      },
      "TempUnit": "C"
    }
    yield mqtt_json_sensor(tasmota_sensor_topic, data)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY)

    # Define reference data.
    reference = {
        u'time': u'2017-10-05T20:39:45Z',
        u'DHT22.Temperature': 33.2,
        u'DHT22.Humidity': 30,
        u'DS18x20.DS1.Temperature': 25.37,
        u'DS18x20.DS2.Temperature': 30.44,
        u'DS18x20.DS3.Temperature': 25.81,
    }

    # Proof that data arrived in InfluxDB.
    record = influx_sensors.get_first_record()
    logger.info('record: %s', json.dumps(record))
    assert record == reference
    yield record


@pytest_twisted.inlineCallbacks
@pytest.mark.tasmota
def test_tasmota_state(machinery, create_influxdb, reset_influxdb):
    """
    Publish a single STATE reading in Tasmota/JSON format
    to MQTT broker, including a timestamp.
    Proof that the reading is processed and stored correctly.

    https://getkotori.org/docs/handbook/decoders/tasmota.html#submit-example-payload
    """

    # Submit a single measurement.
    data = {
      "Time": "2019-06-02T22:13:07",
      "Uptime": "1T18:10:35",
      "Vcc": 3.182,
      "SleepMode": "Dynamic",
      "Sleep": 50,
      "LoadAvg": 19,
      "Wifi": {
        "AP": 1,
        "SSId": "{redacted}",
        "BSSId": "A0:F3:C1:{redacted}",
        "Channel": 1,
        "RSSI": 100,
        "LinkCount": 1,
        "Downtime": "0T00:00:07"
      }
    }
    yield mqtt_json_sensor(tasmota_state_topic, data)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY)

    # Define reference data.
    reference = {
      u'time': u'2019-06-02T20:13:07Z',
      u'Device.Vcc': 3.182,
      u'Device.Sleep': 50,
      u'Device.LoadAvg': 19,
      u'Device.Wifi.Channel': 1,
      u'Device.Wifi.RSSI': 100,
      u'Device.Wifi.LinkCount': 1,
    }

    # Proof that data arrived in InfluxDB.
    record = influx_sensors.get_first_record()
    assert record == reference
    yield record
