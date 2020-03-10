# -*- coding: utf-8 -*-
# (c) 2020 Andreas Motl <andreas@getkotori.org>
import logging

import pytest
import pytest_twisted

from test.resources import influx, PROCESS_DELAY
from test.util import mqtt_sensor, sleep

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
    yield mqtt_sensor(tasmota_sensor_topic, data)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY)

    # Define reference data.
    reference = {
      u'time': u'2019-06-02T20:13:07Z',
      u'AirQuality': 90,
      u'Humidity': 15,
      u'Light': 20,
      u'Noise': 10,
      u'Temperature': 25,
    }

    # Proof that data arrived in InfluxDB.
    record = influx.get_first_record()
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
    yield mqtt_sensor(tasmota_sensor_topic, data)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY)

    # Define reference data.
    reference = {
      u'time': u'2017-02-16T09:13:52Z',
      u'Temperature': 20.6,
    }

    # Proof that data arrived in InfluxDB.
    record = influx.get_first_record()
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
    yield mqtt_sensor(tasmota_state_topic, data)

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
    record = influx.get_first_record()
    assert record == reference
    yield record
