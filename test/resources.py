# -*- coding: utf-8 -*-
# (c) 2020 Andreas Motl <andreas@getkotori.org>
from test.util import InfluxWrapper, GrafanaWrapper

PROCESS_DELAY = 0.1

influx_database = 'mqttkit_1_itest'
influx_measurement = 'foo_bar_sensors'
mqtt_topic = 'mqttkit-1/itest/foo/bar/data.json'
grafana_username = 'admin'
grafana_password = 'admin'
grafana_dashboard = 'mqttkit-1-itest'

influx = InfluxWrapper(database=influx_database, measurement=influx_measurement)
grafana = GrafanaWrapper(grafana_username, grafana_password, database=influx_database, measurement=influx_measurement)
