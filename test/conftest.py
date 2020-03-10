# -*- coding: utf-8 -*-
# (c) 2020 Andreas Motl <andreas@getkotori.org>
"""
# conftest.py: sharing fixture functions
https://docs.pytest.org/en/latest/fixture.html#conftest-py-sharing-fixture-functions
"""
import pytest
import logging

import pytest_twisted

from kotori import KotoriBootloader
from test.util import boot_kotori
from test.resources import influx

logger = logging.getLogger(__name__)


@pytest_twisted.inlineCallbacks
@pytest.fixture(scope="package")
def machinery():


    # Invoke the machinery.
    logger.info('Spinning up machinery')

    #result = yield threads.deferToThread(boot_kotori)
    result = boot_kotori()
    assert isinstance(result, KotoriBootloader)

    #pytest_twisted.blockon(result)
    yield result


create_influxdb = influx.make_create_db()
reset_influxdb = influx.make_reset_measurement()
