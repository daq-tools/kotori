# -*- coding: utf-8 -*-
# (c) 2020-2023 Andreas Motl <andreas@getkotori.org>

from test.util import CrateDBWrapper, InfluxWrapper, GrafanaWrapper

PROCESS_DELAY_MQTT = 0.3
PROCESS_DELAY_HTTP = 0.3


class TestSettings:

    # CrateDB settings.
    cratedb_database = 'mqttkit_2_itest'
    cratedb_databases = ['mqttkit_2_itest', 'mqttkit_2_itest3']
    cratedb_measurement_sensors = 'foo_bar_sensors'
    cratedb_measurement_events = 'foo_bar_events'
    mqtt2_topic_json   = 'mqttkit-2/itest/foo/bar/data.json'
    grafana2_dashboards = ['mqttkit-2-itest', 'mqttkit-2-itest3']

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

    # Per-device entrypoints.
    direct_influx_database            = 'mqttkit_1_devices'
    direct_influx_measurement_sensors = 'default_123e4567_e89b_12d3_a456_426614174000_sensors'
    direct_mqtt_topic_device          = 'mqttkit-1/device/123e4567-e89b-12d3-a456-426614174000/data.json'
    direct_mqtt_topic_channel         = 'mqttkit-1/channel/itest-foo-bar/data.json'
    direct_mqtt_topic_channel_denied  = 'mqttkit-1/channel/another-foo-bar/data.json'
    direct_http_path_device           = '/mqttkit-1/device/123e4567-e89b-12d3-a456-426614174000/data'
    direct_http_path_channel          = '/mqttkit-1/channel/itest-foo-bar/data'


settings = TestSettings

cratedb_sensors = CrateDBWrapper(database=settings.cratedb_database, measurement=settings.cratedb_measurement_sensors)
cratedb_events = CrateDBWrapper(database=settings.cratedb_database, measurement=settings.cratedb_measurement_events)
influx_sensors = InfluxWrapper(database=settings.influx_database, measurement=settings.influx_measurement_sensors)
influx_events = InfluxWrapper(database=settings.influx_database, measurement=settings.influx_measurement_events)
grafana = GrafanaWrapper(settings=settings)

device_influx_sensors = InfluxWrapper(database=settings.direct_influx_database, measurement=settings.direct_influx_measurement_sensors)
