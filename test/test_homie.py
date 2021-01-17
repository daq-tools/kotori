# -*- coding: utf-8 -*-
# (c) 2020-2021 Andreas Motl <andreas@getkotori.org>
import logging

import pytest
import pytest_twisted
from twisted.internet import threads

from test.settings.mqttkit import settings, influx_sensors, PROCESS_DELAY
from test.util import mqtt_json_sensor, sleep

logger = logging.getLogger(__name__)


@pytest_twisted.inlineCallbacks
@pytest.mark.mqtt
@pytest.mark.homie
def test_mqtt_homie(machinery, create_influxdb, reset_influxdb):
    """
    Publish reading like a Homie device in JSON format to MQTT broker
    and proof it is stored in the InfluxDB database.
    """

    # Submit a single measurement, without timestamp.
    data = {
        'temperature': 42.84,
        'humidity': 83.1,
    }
    yield threads.deferToThread(mqtt_json_sensor, settings.mqtt_topic_homie, data)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY)

    # Proof that data arrived in InfluxDB.
    record = influx_sensors.get_first_record()
    del record['time']
    assert record == {u'humidity': 83.1, u'temperature': 42.84}
    yield record
