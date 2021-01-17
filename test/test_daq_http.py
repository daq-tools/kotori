# -*- coding: utf-8 -*-
# (c) 2020-2021 Andreas Motl <andreas@getkotori.org>
import logging

import pytest
import pytest_twisted
from twisted.internet import threads

from test.settings.mqttkit import settings, influx_sensors, PROCESS_DELAY
from test.util import http_json_sensor, http_form_sensor, http_csv_sensor, sleep

logger = logging.getLogger(__name__)


@pytest_twisted.inlineCallbacks
@pytest.mark.http
def test_http_json(machinery, create_influxdb, reset_influxdb):
    """
    Submit single reading in JSON format to HTTP API
    and proof it is stored in the InfluxDB database.
    """

    # Submit a single measurement, without timestamp.
    data = {
        'temperature': 25.26,
        'humidity': 51.8,
    }
    yield threads.deferToThread(http_json_sensor, settings.channel_path_data, data)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY)

    # Proof that data arrived in InfluxDB.
    record = influx_sensors.get_first_record()
    del record['time']
    assert record == {u'temperature': 25.26, u'humidity': 51.8}
    yield record


@pytest_twisted.inlineCallbacks
@pytest.mark.http
def test_http_urlencoded(machinery, create_influxdb, reset_influxdb):
    """
    Submit single reading in ``x-www-form-urlencoded`` format to HTTP API
    and proof it is stored in the InfluxDB database.
    """

    # Submit a single measurement, without timestamp.
    data = {
        'temperature': 25.26,
        'humidity': 51.8,
    }
    yield threads.deferToThread(http_form_sensor, settings.channel_path_data, data)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY)

    # Proof that data arrived in InfluxDB.
    record = influx_sensors.get_first_record()
    del record['time']
    assert record == {u'temperature': 25.26, u'humidity': 51.8}
    yield record


@pytest_twisted.inlineCallbacks
@pytest.mark.http
@pytest.mark.mongodb
def test_http_csv(machinery, create_influxdb, reset_influxdb):
    """
    Submit single reading in CSV format to HTTP API
    and proof it is stored in the InfluxDB database.
    """

    # Submit a single measurement, without timestamp.
    data = {
        'temperature': 25.26,
        'humidity': 51.8,
    }
    yield threads.deferToThread(http_csv_sensor, settings.channel_path_data, data)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY)

    # Proof that data arrived in InfluxDB.
    record = influx_sensors.get_first_record()
    del record['time']
    assert record == {u'temperature': 25.26, u'humidity': 51.8}
    yield record
