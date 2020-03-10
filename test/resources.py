# -*- coding: utf-8 -*-
# (c) 2020 Andreas Motl <andreas@getkotori.org>

from test.util import InfluxWrapper, GrafanaWrapper

PROCESS_DELAY = 0.1


class TestSettings:

    # InfluxDB settings.
    influx_database = 'mqttkit_1_itest'
    influx_measurement = 'foo_bar_sensors'

    # Grafana settings.
    grafana_username = 'admin'
    grafana_password = 'admin'
    grafana_dashboards = ['mqttkit-1-itest']

    # Channel settings.
    mqtt_topic_json = 'mqttkit-1/itest/foo/bar/data.json'
    mqtt_topic_single = 'mqttkit-1/itest/foo/bar/data'
    channel_path = '/mqttkit-1/itest/foo/bar/data'

    def __init__(self):
        pass


settings = TestSettings()

influx = InfluxWrapper(database=settings.influx_database, measurement=settings.influx_measurement)
grafana = GrafanaWrapper(settings=settings)
