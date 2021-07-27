# -*- coding: utf-8 -*-
# (c) 2020-2021 Andreas Motl <andreas@getkotori.org>
import json
import logging

import pytest
import pytest_twisted
from twisted.internet import threads

from test.settings.mqttkit import settings, influx_sensors, PROCESS_DELAY_HTTP
from test.util import http_json_sensor, http_form_sensor, http_csv_sensor, sleep, http_raw

logger = logging.getLogger(__name__)


@pytest_twisted.inlineCallbacks
@pytest.mark.http
def test_http_json_valid(machinery, create_influxdb, reset_influxdb):
    """
    Submit single reading in JSON format to HTTP API
    and proof it is stored in the InfluxDB database.
    """

    # Submit a single measurement, without timestamp.
    data = {
        'temperature': 25.26,
        'humidity': 51.8,
    }
    deferred = threads.deferToThread(http_json_sensor, settings.channel_path_data, data)
    yield deferred

    # Check response.
    response = deferred.result
    assert response.status_code == 200
    assert response.content == json.dumps([{"type": "info", "message": "Received #1 readings"}], indent=4).encode("utf-8")

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY_HTTP)

    # Proof that data arrived in InfluxDB.
    record = influx_sensors.get_first_record()
    del record['time']
    assert record == {u'temperature': 25.26, u'humidity': 51.8}
    yield record


@pytest_twisted.inlineCallbacks
@pytest.mark.http
def test_http_json_invalid(machinery):
    """
    Submit invalid JSON payload as HTTP request to HTTP API and check for appropriate error response.
    """

    # Submit empty request.
    deferred = threads.deferToThread(http_raw, settings.channel_path_data, headers={"Content-Type": "application/json"}, data='foobar')
    yield deferred

    # Check response.
    response = deferred.result
    assert response.status_code == 400
    assert response.content == b'Unhandled exception: Expecting value: line 1 column 1 (char 0)'


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
    deferred = threads.deferToThread(http_form_sensor, settings.channel_path_data, data)
    yield deferred

    # Check response.
    response = deferred.result
    assert response.status_code == 200
    assert response.content == json.dumps([{"type": "info", "message": "Received #1 readings"}], indent=4).encode("utf-8")

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY_HTTP)

    # Proof that data arrived in InfluxDB.
    record = influx_sensors.get_first_record()
    del record['time']
    assert record == {u'temperature': 25.26, u'humidity': 51.8}
    yield record


@pytest_twisted.inlineCallbacks
@pytest.mark.http
@pytest.mark.mongodb
def test_http_csv_valid(machinery, create_influxdb, reset_influxdb):
    """
    Submit single reading in CSV format to HTTP API
    and proof it is stored in the InfluxDB database.
    """

    # Submit a single measurement, without timestamp.
    data = {
        'temperature': 25.26,
        'humidity': 51.8,
    }
    deferred = threads.deferToThread(http_csv_sensor, settings.channel_path_data, data)
    yield deferred

    # Check response.
    response = deferred.result
    assert response.status_code == 200
    assert response.content == json.dumps([
        {"type": "info", "message": "Received header fields ['temperature', 'humidity']"},
        {"type": "info", "message": "Received #1 readings"},
    ], indent=4).encode("utf-8")

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY_HTTP)

    # Proof that data arrived in InfluxDB.
    record = influx_sensors.get_first_record()
    del record['time']
    assert record == {u'temperature': 25.26, u'humidity': 51.8}
    yield record


@pytest_twisted.inlineCallbacks
@pytest.mark.http
@pytest.mark.mongodb
def test_http_csv_invalid(machinery, create_influxdb, reset_influxdb):
    """
    Submit invalid reading in CSV format to HTTP API
    and check for appropriate response.
    """

    # Submit an invalid measurement.
    deferred = threads.deferToThread(http_raw, settings.channel2_path_data, headers={"Content-Type": "text/csv"}, data="foobar")
    yield deferred

    # Check response.
    response = deferred.result
    assert response.status_code == 400
    assert response.content == b"Could not process data, please supply field names via CSV header before sending readings"


@pytest_twisted.inlineCallbacks
@pytest.mark.http
def test_http_empty(machinery):
    """
    Submit empty HTTP request to HTTP API and check for appropriate error response.
    """

    # Submit empty request.
    deferred = threads.deferToThread(http_raw, settings.channel_path_data, headers={"Content-Type": "application/json"}, data=None)
    yield deferred

    # Check response.
    response = deferred.result
    assert response.status_code == 400
    assert response.content == b'Empty request body'


@pytest_twisted.inlineCallbacks
@pytest.mark.http
def test_http_no_content_type(machinery):
    """
    Submit HTTP request without Content-Type to HTTP API and check for appropriate error response.
    """

    # Submit empty request.
    deferred = threads.deferToThread(http_raw, settings.channel_path_data, data="foobar")
    yield deferred

    # Check response.
    response = deferred.result
    assert response.status_code == 415
    assert response.content == b'Unable to handle request without Content-Type'


@pytest_twisted.inlineCallbacks
@pytest.mark.http
def test_http_unknown_content_type(machinery):
    """
    Submit empty HTTP request to HTTP API and check for appropriate error response.
    """

    # Submit empty request.
    deferred = threads.deferToThread(http_raw, settings.channel_path_data, headers={"Content-Type": "foo/bar"}, data="bazqux")
    yield deferred

    # Check response.
    response = deferred.result
    assert response.status_code == 415
    assert response.content == b"Unable to handle Content-Type 'foo/bar'"
