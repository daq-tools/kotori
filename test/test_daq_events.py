# -*- coding: utf-8 -*-
# (c) 2020 Andreas Motl <andreas@getkotori.org>
import logging

import pytest
import pytest_twisted
from twisted.internet import threads

from test.resources import settings, influx_events, PROCESS_DELAY
from test.util import mqtt_json_sensor, sleep

logger = logging.getLogger(__name__)


@pytest_twisted.inlineCallbacks
@pytest.mark.mqtt
@pytest.mark.events
def test_mqtt_to_influxdb_event(machinery, create_influxdb, reset_influxdb_events):
    """
    Publish event in JSON format to MQTT broker
    and proof it is stored in the InfluxDB database.
    """

    # Submit a single measurement, without timestamp.
    data = {
        'title': 'Some event',
        'text': '<a href="https://somewhere.example.org/events?reference=482a38ce-791e-11e6-b152-7cd1c55000be">see also</a>',
        'tags': 'event,alert,important',
        'reference': '482a38ce-791e-11e6-b152-7cd1c55000be',
    }
    yield threads.deferToThread(mqtt_json_sensor, settings.mqtt_topic_event, data)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY)

    # Proof that data arrived in InfluxDB.
    record = influx_events.get_first_record()
    del record['time']
    assert record == data
