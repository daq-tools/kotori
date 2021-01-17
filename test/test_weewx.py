# -*- coding: utf-8 -*-
# (c) 2020-2021 Andreas Motl <andreas@getkotori.org>
import logging

import pytest
import pytest_twisted
from twisted.internet import threads

from test.settings.mqttkit import settings, influx_sensors, PROCESS_DELAY
from test.util import mqtt_json_sensor, sleep

logger = logging.getLogger(__name__)


# The WeeWX decoder listens on the special MQTT topic suffix "/loop".
mqtt_topic = 'mqttkit-1/itest/foo/bar/loop'

# Data payload captured from a Vantage Pro 2 weather station.
data = {
    "windSpeed10_kph": "5.78725803977",
    "monthET": "1.32",
    "highUV": "0.0",
    "cloudbase_meter": "773.082217509",
    "leafTemp1_C": "8.33333333333",
    "rainAlarm": "0.0",
    "pressure_mbar": "948.046280104",
    "rain_cm": "0.0",
    "highRadiation": "0.0",
    "interval_minute": "5.0",
    "barometer_mbar": "1018.35464712",
    "yearRain_cm": "17.2000000043",
    "consBatteryVoltage_volt": "4.72",
    "dewpoint_C": "2.07088485785",
    "insideAlarm": "0.0",
    "inHumidity": "29.0",
    "soilLeafAlarm4": "0.0",
    "sunrise": "1492489200.0",
    "windGust_kph": "9.65608800006",
    "heatindex_C": "3.55555555556",
    "dayRain_cm": "0.0",
    "lowOutTemp": "38.3",
    "outsideAlarm1": "0.0",
    "forecastIcon": "8.0",
    "outsideAlarm2": "0.0",
    "windSpeed_kph": "3.95409343049",
    "forecastRule": "40.0",
    "windrun_km": "1.07449640224",
    "outHumidity": "90.0",
    "stormStart": "1492207200.0",
    "inDewpoint": "45.1231125123",
    "altimeter_mbar": "1016.62778614",
    "windchill_C": "3.55555555556",
    "appTemp_C": "1.26842313302",
    "outTemp_C": "3.55555555556",
    "windGustDir": "275.0",
    "extraAlarm1": "0.0",
    "extraAlarm2": "0.0",
    "extraAlarm3": "0.0",
    "extraAlarm4": "0.0",
    "extraAlarm5": "0.0",
    "extraAlarm6": "0.0",
    "extraAlarm7": "0.0",
    "extraAlarm8": "0.0",
    "humidex_C": "3.55555555556",
    "rain24_cm": "0.88000000022",
    "rxCheckPercent": "87.9791666667",
    "hourRain_cm": "0.0",
    "inTemp_C": "26.8333333333",
    "watertemp": "8.33333333333",
    "trendIcon": "59.7350993377",
    "soilLeafAlarm2": "0.0",
    "soilLeafAlarm3": "0.0",
    "usUnits": "16.0",
    "soilLeafAlarm1": "0.0",
    "leafWet4": "0.0",
    "txBatteryStatus": "0.0",
    "yearET": "4.88",
    "monthRain_cm": "2.94000000074",
    "UV": "0.0",
    "rainRate_cm_per_hour": "0.0",
    "dayET": "0.0",
    "dateTime": "1492467300.0",
    "windDir": "283.55437192",
    "stormRain_cm": "1.72000000043",
    "ET_cm": "0.0",
    "sunset": "1492538940.0",
    "highOutTemp": "38.4",
    "radiation_Wpm2": "0.0"
}


@pytest_twisted.inlineCallbacks
@pytest.mark.mqtt
@pytest.mark.weewx
def test_weewx_mqtt(machinery, create_influxdb, reset_influxdb):
    """
    Publish single reading in JSON format to MQTT broker
    and proof it is stored in the InfluxDB database.
    """

    # Submit a single measurement, without timestamp.
    yield threads.deferToThread(mqtt_json_sensor, settings.mqtt_topic_json, data)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY)

    # Proof that data arrived in InfluxDB.
    record = influx_sensors.get_first_record()

    assert record["time"] == '2017-04-17T22:15:00Z'

    assert record["outTemp_C"] == 3.55555555556
    assert record["windSpeed10_kph"] == 5.78725803977
    assert record["cloudbase_meter"] == 773.082217509
    assert record["consBatteryVoltage_volt"] == 4.72

    yield record
