.. include:: _resources.rst

=============
Kotori README
=============

*Kotori* is a multi-channel, multi-protocol data acquisition and graphing toolkit based on
InfluxDB_, Grafana_, Mosquitto_, Twisted_ and Autobahn_.

It is a convenient component for building telemetry solutions and test benches addressing different
aspects of collecting and storing sensor data from a multitude of data sources and devices.


The framework design has two audiences in mind.


For users
---------
Interactively create data sinks, add decoding- and mapping-rules and finally store data points into InfluxDB_,
a leading open source time series database suitable for realtime analytics and sensor data storage.

Interactively build realtime dashboards to visualize time series data with Grafana_,
an open source, feature rich metrics dashboard and graph editor.


For developers
--------------
Ingest and distribute data between multiple publishers and subscribers across
different devices using the underpinning software bus systems based on

    - MQTT_, the *MQ Telemetry Transport* connectivity protocol.
    - WAMP_, the *Web Application Messaging Protocol*, in turn based on WebSockets_.

Leverage the open infrastructure based on Twisted_ - an event-driven networking engine -
to implement custom software components.
Accept new protocols, write adapters, decoders and handlers for specific devices, data formats
and databases.

