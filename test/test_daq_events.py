# -*- coding: utf-8 -*-
# (c) 2020-2021 Andreas Motl <andreas@getkotori.org>
import logging

import pytest
import pytest_twisted
from twisted.internet import threads

from test.settings.mqttkit import settings, influx_events, PROCESS_DELAY
from test.util import mqtt_json_sensor, sleep, http_json_sensor, http_form_sensor

logger = logging.getLogger(__name__)

event_data = {
    'title': 'Some event',
    'text': '<a href="https://somewhere.example.org/events?reference=482a38ce-791e-11e6-b152-7cd1c55000be">see also</a>',
    'tags': 'event,alert,important',
    'reference': '482a38ce-791e-11e6-b152-7cd1c55000be',
}


@pytest_twisted.inlineCallbacks
@pytest.mark.mqtt
@pytest.mark.events
def test_event_mqtt(machinery, create_influxdb, reset_influxdb_events):
    """
    Publish event in JSON format to MQTT broker
    and proof it is stored in the InfluxDB database.
    """

    # Submit a single event, without timestamp.
    yield threads.deferToThread(mqtt_json_sensor, settings.mqtt_topic_event, event_data)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY)

    # Proof that event arrived in InfluxDB.
    record = influx_events.get_first_record()
    del record['time']
    assert record == event_data


@pytest_twisted.inlineCallbacks
@pytest.mark.http
@pytest.mark.events
def test_event_http_json(machinery, create_influxdb, reset_influxdb):
    """
    Submit event in JSON format to HTTP API
    and proof it is stored in the InfluxDB database.
    """

    # Submit a single event, without timestamp.
    yield threads.deferToThread(http_json_sensor, settings.channel_path_event, event_data)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY)

    # Proof that event arrived in InfluxDB.
    record = influx_events.get_first_record()
    del record['time']
    assert record == event_data
    yield record


@pytest_twisted.inlineCallbacks
@pytest.mark.http
@pytest.mark.events
def test_event_http_urlencoded(machinery, create_influxdb, reset_influxdb):
    """
    Submit event in ``x-www-form-urlencoded`` format to HTTP API
    and proof it is stored in the InfluxDB database.
    """

    # Submit a single event, without timestamp.
    yield threads.deferToThread(http_form_sensor, settings.channel_path_event, event_data)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY)

    # Proof that event arrived in InfluxDB.
    record = influx_events.get_first_record()
    del record['time']
    assert record == event_data
    yield record
