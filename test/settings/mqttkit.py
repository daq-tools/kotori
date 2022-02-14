# -*- coding: utf-8 -*-
# (c) 2020 Andreas Motl <andreas@getkotori.org>

from test.util import InfluxWrapper, GrafanaWrapper

PROCESS_DELAY_MQTT = 0.3
PROCESS_DELAY_HTTP = 0.3


class TestSettings:

    # InfluxDB settings.
    influx_database = 'mqttkit_1_itest'
    influx_databases = ['mqttkit_1_itest', 'mqttkit_1_itest3']
    influx_measurement_sensors = 'foo_bar_sensors'
    influx_measurement_events = 'foo_bar_events'

    # Grafana settings.
    grafana_username = 'admin'
    grafana_password = 'admin'
    grafana_dashboards = ['mqttkit-1-itest', 'mqttkit-1-itest3']

    # MQTT channel settings.
    mqtt_topic_single = 'mqttkit-1/itest/foo/bar/data'
    mqtt_topic_json   = 'mqttkit-1/itest/foo/bar/data.json'
    mqtt_topic2_json   = 'mqttkit-1/itest/foo/bar2/data.json'
    mqtt_topic3_json   = 'mqttkit-1/itest3/foo/bar/data.json'
    mqtt_topic_event  = 'mqttkit-1/itest/foo/bar/event.json'
    mqtt_topic_homie  = 'mqttkit-1/itest/foo/bar/data/__json__'
    mqtt_topic_json_legacy = 'mqttkit-1/itest/foo/bar/message-json'

    # HTTP channel settings.
    channel_path_data    = '/mqttkit-1/itest/foo/bar/data'
    channel2_path_data   = '/mqttkit-1/itest/foo/bar2/data'
    channel_path_event   = '/mqttkit-1/itest/foo/bar/event'
    channel_path_airrohr = '/mqttkit-1/itest/foo/bar/custom/airrohr'
    channel_path_ttn     = '/mqttkit-1/ttn'


settings = TestSettings

influx_sensors = InfluxWrapper(database=settings.influx_database, measurement=settings.influx_measurement_sensors)
influx_events = InfluxWrapper(database=settings.influx_database, measurement=settings.influx_measurement_events)
grafana = GrafanaWrapper(settings=settings)
