# -*- coding: utf-8 -*-
# (c) 2020-2021 Andreas Motl <andreas@getkotori.org>
import logging

import pytest
import pytest_twisted
from twisted.internet import threads

from test.settings.mqttkit import settings, PROCESS_DELAY
from test.util import sleep, http_json_sensor, http_get_data

logger = logging.getLogger(__name__)


@pytest_twisted.inlineCallbacks
@pytest.mark.http
@pytest.mark.export
def test_export(machinery, create_influxdb, reset_influxdb):
    """
    Submit single reading in JSON format to HTTP API and proof
    it can be retrieved back from the HTTP API in different formats.
    """

    # Submit a single measurement, with timestamp.
    data = {
        'time': 1583810982,
        'temperature': 25.26,
        'humidity': 51.8,
    }
    yield threads.deferToThread(http_json_sensor, settings.channel_path_data, data)

    # Wait for some time to process the message.
    yield sleep(PROCESS_DELAY)

    # Proof that data is available via HTTP API.
    ts_from = '2020-03-10T00:00:00.000Z'
    ts_to = '2020-03-10T23:59:59.000Z'

    # CSV format.
    deferred = threads.deferToThread(http_get_data, settings.channel_path_data, format='csv', ts_from=ts_from, ts_to=ts_to)
    yield deferred
    assert deferred.result == 'time,humidity,temperature\n2020-03-10T03:29:42.000000Z,51.8,25.26\n'

    # TXT format (same as CSV).
    deferred = threads.deferToThread(http_get_data, settings.channel_path_data, format='txt', ts_from=ts_from, ts_to=ts_to)
    yield deferred
    assert deferred.result == 'time,humidity,temperature\n2020-03-10T03:29:42.000000Z,51.8,25.26\n'

    # JSON format.
    deferred = threads.deferToThread(http_get_data, settings.channel_path_data, format='json', ts_from=ts_from, ts_to=ts_to)
    yield deferred
    assert deferred.result == '[{"time":"2020-03-10T03:29:42.000Z","humidity":51.8,"temperature":25.26}]'

    # XLSX format.
    deferred = threads.deferToThread(http_get_data, settings.channel_path_data, format='xlsx', ts_from=ts_from, ts_to=ts_to)
    yield deferred
    assert deferred.result.startswith(b'PK\x03\x04\x14\x00\x00\x00\x08\x00')

    # HTML format.
    deferred = threads.deferToThread(http_get_data, settings.channel_path_data, format='html', ts_from=ts_from, ts_to=ts_to)
    yield deferred
    assert \
        '<html>' in deferred.result and \
        '<th>temperature</th>' in deferred.result and \
        '<td>25.26</td>' in deferred.result

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

    # NetCDF format.
    deferred = threads.deferToThread(http_get_data, settings.channel_path_data, format='nc', ts_from=ts_from, ts_to=ts_to)
    yield deferred
    assert deferred.result.startswith(b'\x89HDF\r\n\x1a\n\x00\x00\x00\x00\x00')

    # Datatables HTML.
    deferred = threads.deferToThread(http_get_data, settings.channel_path_data, format='dt', ts_from=ts_from, ts_to=ts_to)
    yield deferred
    assert b"cdn.datatables.net" in deferred.result
