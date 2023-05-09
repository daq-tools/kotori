# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas@getkotori.org>
"""
Test the TTS-/TTN-webhook receiver implementation.
TTS/TTN means "The Things Stack" / "The Things Network".

Usage
=====
::

    source .venv/bin/activate
    pytest -m ttn

References
==========
- https://www.thethingsindustries.com/docs/the-things-stack/concepts/data-formats/#uplink-messages
- https://www.thethingsindustries.com/docs/integrations/webhooks/
- https://community.hiveeyes.org/t/more-data-acquisition-payload-formats-for-kotori/1421
- https://community.hiveeyes.org/t/tts-ttn-daten-an-kotori-weiterleiten/1422/34
"""
import logging

from kotori.daq.decoder import TheThingsStackDecoder
from test.settings.basic import (
    settings,
    influx_sensors,
    create_influxdb,
    reset_influxdb,
    reset_grafana,
    PROCESS_DELAY_MQTT,
)
from test.util import http_json_sensor, read_jsonfile, sleep, read_file

import pytest
import pytest_twisted
from twisted.internet import threads

logger = logging.getLogger(__name__)


def make_testcases():
    """
    Define different test cases with in/out pairs.
    """
    return [
        {
            "in": read_jsonfile("test_tts_ttn_full.json"),
            "out": {
                "device_id": "foo-bar-baz",
                "time": "2022-01-19T19:02:34.007345Z",
                "analog_in_1": 59.04,
                "analog_in_2": 58.69,
                "analog_in_3": 3.49,
                "relative_humidity_2": 78.5,
                "temperature_2": 4.2,
                "temperature_3": 3.4,
                "bw": 125.0,
                "counter": 2289.0,
                'freq': 868.5,
                'sf': 7.0,
                'gtw_count': 2.0,
                'gw_elsewhere-ffp_rssi': -90.0,
                'gw_elsewhere-ffp_snr': 7.0,
                'gw_somewhere-ffp_rssi': -107.0,
                'gw_somewhere-ffp_snr': -6.5,
            },
        },
        {
            "in": read_jsonfile("test_tts_ttn_minimal.json"),
            "__delete__": ["time"],
            "out": {"temperature_1": 53.3, "voltage_4": 3.3},
        },
    ]


@pytest_twisted.inlineCallbacks
@pytest.mark.http
@pytest.mark.tts
@pytest.mark.ttn
@pytest.mark.parametrize("testcase", make_testcases())
def test_tts_ttn_http_json_full(
    testcase, machinery_basic, create_influxdb, reset_influxdb
):
    """
    Submit single reading in TTS/TTN webhook JSON format to HTTP API,
    and verify it was correctly stored in the InfluxDB database.
    """

    data_in = testcase["in"]
    data_out = testcase["out"]

    # Submit a single measurement, without timestamp.
    yield threads.deferToThread(http_json_sensor, settings.channel_path_data, data_in)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY_MQTT)
    yield sleep(PROCESS_DELAY_MQTT)

    # Proof that data arrived in InfluxDB properly.
    record = influx_sensors.get_first_record()

    # Optionally delete specific fields, to make comparison work.
    if "__delete__" in testcase:
        for delete_field in testcase["__delete__"]:
            del record[delete_field]

    # Verify the records looks like expected.
    assert record == data_out
    yield record


@pytest.mark.tts
@pytest.mark.ttn
def test_ttn_decode_minimal():
    payload = read_file("test_tts_ttn_minimal.json").decode("utf-8")
    decoded = dict(TheThingsStackDecoder.decode(payload))
    assert decoded == {
        "temperature_1": 53.3,
        "voltage_4": 3.3,
    }


@pytest.mark.tts
@pytest.mark.ttn
def test_ttn_decode_full():
    payload = read_file("test_tts_ttn_full.json").decode("utf-8")
    decoded = dict(TheThingsStackDecoder.decode(payload))
    assert decoded == {
        "device_id": "foo-bar-baz",
        "timestamp": "2022-01-19T19:02:34.007345025Z",
        "analog_in_1": 59.04,
        "analog_in_2": 58.69,
        "analog_in_3": 3.49,
        "relative_humidity_2": 78.5,
        "temperature_2": 4.2,
        "temperature_3": 3.4,
        "bw": 125.0,
        "counter": 2289,
        'freq': 868.5,
        'sf': 7,
        'gtw_count': 2,
        'gw_elsewhere-ffp_rssi': -90,
        'gw_elsewhere-ffp_snr': 7,
        'gw_somewhere-ffp_rssi': -107,
        'gw_somewhere-ffp_snr': -6.5,
    }
