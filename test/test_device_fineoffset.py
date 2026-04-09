import json
import logging

from test.settings.mqttkit import PROCESS_DELAY_HTTP, influx_sensors, settings, grafana
from test.util import http_form_sensor, sleep

import pytest
import pytest_twisted
from twisted.internet import threads


logger = logging.getLogger(__name__)


@pytest_twisted.inlineCallbacks
@pytest.mark.http
@pytest.mark.grafana
def test_device_ecowitt_post(machinery, create_influxdb, reset_influxdb, reset_grafana):
    """
    Submit single reading in ``x-www-form-urlencoded`` format to HTTP API
    and proof it is stored in the InfluxDB database.
    """

    # Submit a single measurement.
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

    # Standard values, converted to "metric" unit system.
    # Temperature converted from 48.4 degrees Fahrenheit, wind speed converted
    # from 1.12 mph, humidity untouched.
    assert round(record["temp"], 1) == 9.1
    assert round(record["windspeed"], 1) == 1.8
    assert record["humidity"] == 80.0

    # Verify the data includes additional computed fields.
    assert round(record["dewpoint"], 1) == 5.8
    assert round(record["feelslike"], 1) == 9.1

    # Only newer releases of `ecowitt2mqtt` will compute those fields.
    if "frostpoint" in record:
        assert round(record["frostpoint"], 1) == 4.7
        assert record["frostrisk"] == "No risk"
        assert record["thermalperception"] == "Dry"

    # Make sure those fields got purged, so they don't leak into public data.
    assert "PASSKEY" not in record
    assert "stationtype" not in record
    assert "model" not in record

    # Timestamp field also gets removed, probably to avoid ambiguities.
    assert "dateutc" not in record

    # Proof that Grafana is well provisioned.
    logger.info('Grafana: Checking datasource')
    assert settings.influx_database in grafana.get_datasource_names()

    logger.info('Grafana: Retrieving dashboard')
    dashboard_name = settings.grafana_dashboards[0]
    dashboard = grafana.get_dashboard_by_name(dashboard_name)

    logger.info('Grafana: Checking dashboard layout')
    targets = dashboard["rows"][0]["panels"][0]["targets"]
    assert targets[0]["measurement"] == settings.influx_measurement_sensors

    fieldnames = []
    for target in targets:
        fieldnames.append(target.get("fields")[0]["name"])

    # Verify that text fields are not part of the graph. Otherwise, Grafana would croak like:
    # - InfluxDB Error: unsupported mean iterator type: *query.stringInterruptIterator
    # - InfluxDB Error: not executed
    assert "batt1" not in fieldnames, "'batt1' should have been removed, because it is a text field"
    assert "frostrisk" not in fieldnames, "'frostrisk' should have been removed, because it is a text field"
