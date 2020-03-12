# -*- coding: utf-8 -*-
# (c) 2020 Andreas Motl <andreas@getkotori.org>

from test.util import InfluxWrapper, GrafanaWrapper

PROCESS_DELAY = 0.1


class BasicSettings:

    # InfluxDB settings.
    influx_database = 'basic_node42'
    influx_measurement_sensors = 'sensors'
    influx_measurement_events = 'events'

    # Grafana settings.
    grafana_username = 'admin'
    grafana_password = 'admin'
    grafana_dashboards = ['basic-node42']

    # MQTT channel settings.
    mqtt_topic_single = 'basic/node42/data'
    mqtt_topic_json   = 'basic/node42/data.json'
    mqtt_topic_event  = 'basic/node42/event.json'
    mqtt_topic_homie  = 'basic/node42/data/__json__'
    mqtt_topic_json_legacy = 'basic/node42/message-json'

    # HTTP channel settings.
    channel_path_data    = '/basic/node42/data'
    channel_path_event   = '/basic/node42/event'
    channel_path_airrohr = '/basic/node42/custom/airrohr'


settings = BasicSettings

influx_sensors = InfluxWrapper(database=settings.influx_database, measurement=settings.influx_measurement_sensors)
influx_events = InfluxWrapper(database=settings.influx_database, measurement=settings.influx_measurement_events)
grafana = GrafanaWrapper(settings=settings)

create_influxdb = influx_sensors.make_create_db()
reset_influxdb = influx_sensors.make_reset_measurement()
reset_grafana = grafana.make_reset()
