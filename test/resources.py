# -*- coding: utf-8 -*-
# (c) 2020 Andreas Motl <andreas@getkotori.org>
from bunch import Bunch

from test.util import InfluxWrapper, GrafanaWrapper

PROCESS_DELAY = 0.1

settings = Bunch(
    influx_database='mqttkit_1_itest',
    influx_measurement='foo_bar_sensors',
    mqtt_topic='mqttkit-1/itest/foo/bar/data.json',
    grafana_username='admin',
    grafana_password='admin',
    grafana_dashboards=['mqttkit-1-itest'],
)

influx = InfluxWrapper(database=settings.influx_database, measurement=settings.influx_measurement)
grafana = GrafanaWrapper(settings=settings)
