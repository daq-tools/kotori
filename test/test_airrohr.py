# -*- coding: utf-8 -*-
# (c) 2020-2021 Andreas Motl <andreas@getkotori.org>
import logging

import pytest
import pytest_twisted
from twisted.internet import threads

from test.settings.basic import settings, influx_sensors, grafana, create_influxdb, reset_influxdb, reset_grafana, PROCESS_DELAY
from test.util import http_json_sensor, sleep

logger = logging.getLogger(__name__)


# https://community.hiveeyes.org/t/more-data-acquisition-payload-formats-for-kotori/1421/2


data_in = {
  "esp8266id": 12041741,
  "sensordatavalues": [
    {
      "value_type": "SDS_P1",
      "value": "35.67"
    },
    {
      "value_type": "SDS_P2",
      "value": "17.00"
    },
    {
      "value_type": "BME280_temperature",
      "value": "-2.83"
    },
    {
      "value_type": "BME280_humidity",
      "value": "66.73"
    },
    {
      "value_type": "BME280_pressure",
      "value": "100535.97"
    },
    {
      "value_type": "samples",
      "value": "3016882"
    },
    {
      "value_type": "min_micro",
      "value": "77"
    },
    {
      "value_type": "max_micro",
      "value": "26303"
    },
    {
      "value_type": "signal",
      "value": "-66"
    }
  ],
  "software_version": "NRZ-2018-123B"
}


data_out = {
  u'SDS_P1': 35.67,
  u'SDS_P2': 17.00,
  u'BME280_temperature': -2.83,
  u'BME280_humidity': 66.73,
  u'BME280_pressure': 100535.97,
  u'samples': 3016882,
  u'min_micro': 77,
  u'max_micro': 26303,
  u'signal': -66,
}


create_influxdb = influx_sensors.make_create_db()
reset_influxdb = influx_sensors.make_reset_measurement()


@pytest_twisted.inlineCallbacks
@pytest.mark.http
@pytest.mark.airrohr
def test_airrohr_http_json(machinery, create_influxdb, reset_influxdb):
    """
    Submit single reading in Airrohr JSON format to HTTP API
    and proof it is stored in the InfluxDB database.
    """

    # Submit a single measurement, without timestamp.
    yield threads.deferToThread(http_json_sensor, settings.channel_path_airrohr, data_in)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY)

    # Proof that data arrived in InfluxDB.
    record = influx_sensors.get_first_record()
    del record['time']
    assert record == data_out
    yield record
