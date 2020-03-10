# -*- coding: utf-8 -*-
# (c) 2020 Andreas Motl <andreas@getkotori.org>
import logging

import pytest
import pytest_twisted
from twisted.internet import threads

from test.resources import settings, PROCESS_DELAY
from test.util import sleep, http_json_sensor, http_get_data

logger = logging.getLogger(__name__)


@pytest_twisted.inlineCallbacks
@pytest.mark.http
@pytest.mark.export
def test_export_csv(machinery, create_influxdb, reset_influxdb):
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

    # CSV format.
    deferred = threads.deferToThread(http_get_data, settings.channel_path_data, format='csv')
    yield deferred
    assert deferred.result == 'time,humidity,temperature\n2020-03-10T03:29:42.000000Z,51.8,25.26\n'

    # TXT format (same as CSV).
    deferred = threads.deferToThread(http_get_data, settings.channel_path_data, format='txt')
    yield deferred
    assert deferred.result == 'time,humidity,temperature\n2020-03-10T03:29:42.000000Z,51.8,25.26\n'

    # JSON format.
    deferred = threads.deferToThread(http_get_data, settings.channel_path_data, format='json')
    yield deferred
    assert deferred.result == '[{"time":"2020-03-10T03:29:42.000Z","humidity":51.8,"temperature":25.26}]'

    # XLSX format.
    deferred = threads.deferToThread(http_get_data, settings.channel_path_data, format='xlsx')
    yield deferred
    assert deferred.result.startswith(b'PK\x03\x04\x14\x00\x00\x00\x08\x00')

    # HTML format.
    deferred = threads.deferToThread(http_get_data, settings.channel_path_data, format='html')
    yield deferred
    assert \
        '<html>' in deferred.result and \
        '<th>temperature</th>' in deferred.result and \
        '<td>25.26</td>' in deferred.result
