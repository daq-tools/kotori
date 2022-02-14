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
from test.settings.basic import (
    settings,
    influx_sensors,
    create_influxdb,
    reset_influxdb,
    reset_grafana,
    PROCESS_DELAY_MQTT,
)
from test.util import http_json_sensor, read_jsonfile, sleep

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
                "time": "2022-01-19T19:02:34.007345Z",
                "analog_in_1": 59.04,
                "analog_in_2": 58.69,
                "analog_in_3": 3.49,
                "relative_humidity_2": 78.5,
                "temperature_2": 4.2,
                "temperature_3": 3.4,
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
def test_tts_ttn_http_json_decoder(testcase, machinery_basic, create_influxdb, reset_influxdb):
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


@pytest_twisted.inlineCallbacks
@pytest.mark.http
@pytest.mark.tts
@pytest.mark.ttn
@pytest.mark.amo
def test_tts_ttn_http_json_forwarder(machinery, create_influxdb, reset_influxdb):
    """
    Accept all requests to the `/api/ttn` URL suffix in TTS/TTN webhook JSON format
    and proof it is stored in the InfluxDB database.
    """

    from test.settings.mqttkit import settings as mqttkit_settings

    # Submit a single measurement, without timestamp.
    baseurl = mqttkit_settings.channel_path_ttn
    device_id = "itest-foo-bar"
    yield threads.deferToThread(http_json_sensor, f"{baseurl}/{device_id}/uplinks", data_in)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY_MQTT)
    yield sleep(PROCESS_DELAY_MQTT)

    # Proof that data arrived in InfluxDB properly.
    record = influx_sensors.get_first_record()
    assert record == data_out
    yield record
