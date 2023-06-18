# -*- coding: utf-8 -*-
# (c) 2020-2023 Andreas Motl <andreas@getkotori.org>
import functools
import json
import logging

import io
import pandas as pd
import pytest
import pytest_twisted
from twisted.internet import threads

from test.settings.mqttkit import settings, PROCESS_DELAY_MQTT
from test.util import sleep, http_json_sensor, http_get_data
from pandas.testing import assert_frame_equal
from datadiff.tools import assert_equal

logger = logging.getLogger(__name__)


# Define date ranges for querying.
ts_from = '2020-03-10T00:00:00.000Z'
ts_to = '2020-03-10T23:59:59.000Z'


@pytest_twisted.inlineCallbacks
@pytest.mark.http
@pytest.mark.export
@pytest.mark.influxdb
def test_export_influxdb_general(machinery, create_influxdb, reset_influxdb):
    """
    Submit single reading in JSON format to HTTP API and proof
    it can be retrieved back from the HTTP API in different formats.

    This uses InfluxDB as timeseries database.
    """

    channel_path = settings.channel_path_data
    http_submit = functools.partial(http_json_sensor, port=24642)
    http_fetch = functools.partial(http_get_data, port=24642)

    yield verify_export_general(channel_path, http_submit, http_fetch)


@pytest_twisted.inlineCallbacks
def verify_export_general(channel_path, http_submit, http_fetch):

    # Submit a single measurement, with timestamp.
    data = {
        'time': 1583810982,
        'temperature': 25.26,
        'humidity': 51.8,
    }
    yield threads.deferToThread(http_submit, channel_path, data)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY_MQTT)

    # Reference DataFrame to compare with.
    df_should = pd.DataFrame([[pd.to_datetime("2020-03-10T03:29:42.000000Z"), 51.8, 25.26]], columns=["time", "humidity", "temperature"])

    # CSV format.
    deferred = threads.deferToThread(http_fetch, channel_path, format='csv', ts_from=ts_from, ts_to=ts_to)
    yield deferred
    result = pd.read_csv(io.StringIO(deferred.result), parse_dates=["time"])
    assert_frame_equal(result, df_should, check_names=False, check_like=True, check_datetimelike_compat=True)

    # TXT format (same as CSV).
    deferred = threads.deferToThread(http_fetch, channel_path, format='txt', ts_from=ts_from, ts_to=ts_to)
    yield deferred
    result = pd.read_csv(io.StringIO(deferred.result), parse_dates=["time"])
    assert_frame_equal(result, df_should, check_names=False, check_like=True, check_datetimelike_compat=True)

    # JSON format.
    deferred = threads.deferToThread(http_fetch, channel_path, format='json', ts_from=ts_from, ts_to=ts_to)
    yield deferred
    result = json.loads(deferred.result)
    should = [{"time": "2020-03-10T03:29:42.000Z", "humidity": 51.8, "temperature": 25.26}]
    assert_equal(result, should)

    # XLSX format.
    deferred = threads.deferToThread(http_fetch, channel_path, format='xlsx', ts_from=ts_from, ts_to=ts_to)
    yield deferred
    assert deferred.result.startswith(b'PK\x03\x04\x14\x00\x00\x00\x08\x00')

    # HTML format.
    deferred = threads.deferToThread(http_fetch, channel_path, format='html', ts_from=ts_from, ts_to=ts_to)
    yield deferred
    assert \
        '<html>' in deferred.result and \
        '<th>temperature</th>' in deferred.result and \
        '<td>25.26</td>' in deferred.result and \
        '<th>humidity</th>' in deferred.result and \
        '<td>51.8</td>' in deferred.result

    # NetCDF format.
    deferred = threads.deferToThread(http_fetch, channel_path, format='nc', ts_from=ts_from, ts_to=ts_to)
    yield deferred
    assert deferred.result.startswith(b'\x89HDF\r\n\x1a\n\x02\x08\x08\x00\x00\x00')

    # Datatables HTML.
    deferred = threads.deferToThread(http_fetch, channel_path, format='dt', ts_from=ts_from, ts_to=ts_to)
    yield deferred
    assert b"cdn.datatables.net" in deferred.result


@pytest_twisted.inlineCallbacks
@pytest.mark.http
@pytest.mark.export
def test_export_hdf5(machinery, create_influxdb, reset_influxdb):
    """
    Submit single reading in JSON format to HTTP API and proof
    it can be retrieved back from the HTTP API in HDF5 format.
    """

    pytest.importorskip("tables", reason="Packages `h5py` and `tables` not available for Python 3.11 yet")

    # Submit a single measurement, with timestamp.
    data = {
        'time': 1583810982,
        'temperature': 25.26,
        'humidity': 51.8,
    }
    yield threads.deferToThread(http_json_sensor, settings.channel_path_data, data)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY_MQTT)

    # HDF5 format.
    deferred = threads.deferToThread(http_get_data, settings.channel_path_data, format='hdf5', ts_from=ts_from, ts_to=ts_to)
    yield deferred
    assert deferred.result.startswith(b'\x89HDF\r\n\x1a\n\x00\x00\x00\x00\x00')

    import h5py
    from io import BytesIO
    from pandas import array
    hdf = h5py.File(BytesIO(deferred.result), "r")
    assert hdf["/itest_foo_bar/table"].attrs.get("NROWS") == 1
    assert hdf["/itest_foo_bar/table"].attrs.get("index_kind") == b"datetime64"
    assert hdf["/itest_foo_bar/table"].attrs.get("humidity_dtype") == b"float64"
    assert hdf["/itest_foo_bar/table"].attrs.get("temperature_dtype") == b"float64"
    assert hdf["/itest_foo_bar/table"].shape == (1,)
    assert hdf["/itest_foo_bar/table"][()] == array(
        [(1583810982000000000, 51.8, 25.26)],
        dtype=[('index', '<i8'), ('humidity', '<f8'), ('temperature', '<f8')])
