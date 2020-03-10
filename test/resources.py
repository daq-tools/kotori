# -*- coding: utf-8 -*-
# (c) 2020 Andreas Motl <andreas@getkotori.org>
from test.util import InfluxWrapper

influx_database = 'mqttkit_1_itest'
influx_measurement = 'foo_bar_sensors'
mqtt_topic = 'mqttkit-1/itest/foo/bar/data.json'

influx = InfluxWrapper(database=influx_database, measurement=influx_measurement)
