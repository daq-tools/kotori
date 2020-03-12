# -*- coding: utf-8 -*-
# (c) 2020 Andreas Motl <andreas@getkotori.org>

from test.util import InfluxWrapper, GrafanaWrapper

PROCESS_DELAY = 0.1


class TestSettings:

    # InfluxDB settings.
    influx_database = 'mqttkit_1_itest'
    influx_measurement_sensors = 'foo_bar_sensors'
    influx_measurement_events = 'foo_bar_events'

    # Grafana settings.
    grafana_username = 'admin'
    grafana_password = 'admin'
    grafana_dashboards = ['mqttkit-1-itest']

    # MQTT channel settings.
    mqtt_topic_single = 'mqttkit-1/itest/foo/bar/data'
    mqtt_topic_json   = 'mqttkit-1/itest/foo/bar/data.json'
    mqtt_topic_event  = 'mqttkit-1/itest/foo/bar/event.json'
    mqtt_topic_homie  = 'mqttkit-1/itest/foo/bar/data/__json__'
    mqtt_topic_json_legacy = 'mqttkit-1/itest/foo/bar/message-json'

    # HTTP channel settings.
    channel_path_data    = '/mqttkit-1/itest/foo/bar/data'
    channel_path_event   = '/mqttkit-1/itest/foo/bar/event'
    channel_path_airrohr = '/mqttkit-1/itest/foo/bar/custom/airrohr'


settings = TestSettings

influx_sensors = InfluxWrapper(database=settings.influx_database, measurement=settings.influx_measurement_sensors)
influx_events = InfluxWrapper(database=settings.influx_database, measurement=settings.influx_measurement_events)
grafana = GrafanaWrapper(settings=settings)
