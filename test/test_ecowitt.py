import json
from test.settings.mqttkit import PROCESS_DELAY_HTTP, influx_sensors, settings
from test.util import http_form_sensor, sleep

import pytest
import pytest_twisted
from twisted.internet import threads


@pytest_twisted.inlineCallbacks
@pytest.mark.http
def test_ecowitt_post(machinery, create_influxdb, reset_influxdb):
    """
    Submit single reading in ``x-www-form-urlencoded`` format to HTTP API
    and proof it is stored in the InfluxDB database.
    """

    # Submit a single measurement, without timestamp.
    data = {
        "PASSKEY": "B950C...[obliterated]",
        "stationtype": "EasyWeatherPro_V5.0.6",
        "runtime": "456128",
        "dateutc": "2023-02-20 16:02:19",
        "tempinf": "69.8",
        "humidityin": "47",
        "baromrelin": "29.713",
        "baromabsin": "29.713",
        "tempf": "48.4",
        "humidity": "80",
        "winddir": "108",
        "windspeedmph": "1.12",
        "windgustmph": "4.92",
        "maxdailygust": "12.97",
        "solarradiation": "1.89",
        "uv": "0",
        "rainratein": "0.000",
        "eventrainin": "0.000",
        "hourlyrainin": "0.000",
        "dailyrainin": "0.028",
        "weeklyrainin": "0.098",
        "monthlyrainin": "0.909",
        "yearlyrainin": "0.909",
        "temp1f": "45.0",
        "humidity1": "90",
        "soilmoisture1": "46",
        "soilmoisture2": "53",
        "tf_ch1": "41.9",
        "rrain_piezo": "0.000",
        "erain_piezo": "0.000",
        "hrain_piezo": "0.000",
        "drain_piezo": "0.028",
        "wrain_piezo": "0.043",
        "mrain_piezo": "0.492",
        "yrain_piezo": "0.492",
        "wh65batt": "0",
        "wh25batt": "0",
        "batt1": "0",
        "soilbatt1": "1.6",
        "soilbatt2": "1.6",
        "tf_batt1": "1.60",
        "wh90batt": "3.04",
        "freq": "868M",
        "model": "HP1000SE-PRO_Pro_V1.8.5",
    }
    deferred = threads.deferToThread(http_form_sensor, settings.channel_path_data, data)
    yield deferred

    # Check response.
    response = deferred.result
    assert response.status_code == 200
    assert response.content == json.dumps(
        [{"type": "info", "message": "Received #1 readings"}], indent=4
    ).encode("utf-8")

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY_HTTP)

    # Proof that data arrived in InfluxDB.
    record = influx_sensors.get_first_record()

    assert record["tempf"] == 48.4
    assert record["humidity"] == 80.0
    assert record["model"] == "HP1000SE-PRO_Pro_V1.8.5"

    # Make sure this will not be public.
    assert "PASSKEY" not in record

    yield record
