# -*- coding: utf-8 -*-
# (c) 2020-2021 Andreas Motl <andreas@getkotori.org>
"""
# conftest.py: sharing fixture functions
https://docs.pytest.org/en/latest/fixture.html#conftest-py-sharing-fixture-functions
"""
import pytest
import logging

import pytest_twisted

from kotori import KotoriBootloader
from test.util import boot_kotori, sleep
from test.settings.mqttkit import influx_sensors, influx_events, grafana

logger = logging.getLogger(__name__)

STARTUP_DELAY = 1.5

# Disable ellipsis truncation
# https://stackoverflow.com/questions/19171554/preventing-truncation-of-long-strings-in-pytest/60321834#60321834
#from _pytest.assertion import truncate
#truncate.DEFAULT_MAX_LINES = 9999
#truncate.DEFAULT_MAX_CHARS = 9999


def create_machinery(config, scope="package"):

    @pytest_twisted.inlineCallbacks
    @pytest.fixture(scope=scope)
    def machinery():

        # Invoke the machinery.
        logger.info('Spinning up machinery')

        #result = yield threads.deferToThread(boot_kotori)
        result = boot_kotori(config)
        assert isinstance(result, KotoriBootloader)

        logger.info(f"Delaying for {STARTUP_DELAY} seconds to wait for the machinery to start")
        waiter = sleep(STARTUP_DELAY)
        pytest_twisted.blockon(waiter)

        logger.info('Machinery is ready')
        yield result

    return machinery


machinery = create_machinery('./etc/test/main.ini')
create_influxdb = influx_sensors.make_create_db()
reset_influxdb = influx_sensors.make_reset_measurement()
reset_grafana = grafana.make_reset()
reset_influxdb_events = influx_events.make_reset_measurement()

machinery_basic = create_machinery('./etc/test/basic.ini')
