.. include:: _resources.rst

=============
Kotori README
=============

    *Kotori* is a multi-channel, multi-protocol data acquisition and graphing toolkit
    based on InfluxDB_, Grafana_, Mosquitto_ and Twisted_.

    It is a convenient component for building flexible telemetry solutions and test benches
    by addressing different aspects of collecting and storing sensor data from a
    multitude of data sources and devices.

By acting as a mediator between components, it does:

    - receive data from various types of channels: MQTT, UDP, HTTP
    - forward data to different kinds of data stores: TSDB, RDBMS, NoSQL
    - control a connected Grafana instance by automatically creating dashboards
      based on the arriving data


----

The design of Kotori has two audiences in mind.


For users
---------
Interactively build appealing dashboards to visualize time series data with Grafana_,
an open source, feature rich metrics dashboard and graph editor.

.. Interactively create data sinks, add decoding- and mapping-rules and

For developers
--------------
Ingest and distribute data between multiple publishers and subscribers across
different devices using the underpinning software bus systems based on

    - MQTT_, the *MQ Telemetry Transport* connectivity protocol.
    - WAMP_, the *Web Application Messaging Protocol*, in turn based on WebSockets_.

- Leverage the open infrastructure based on Twisted_ - an event-driven networking engine -
  to implement custom software components.
- Store data points into InfluxDB_, a leading open source time series database suitable
  for realtime analytics and sensor data storage.
- Precisely control which kind of dashboards are automatically created in Grafana when data arrives.
- Listen and talk to a huge amount of IoT devices speaking MQTT_.
- Talk to thousands of Browsers in a bidirectional way using the WAMP_ software bus.
- Accept new protocols, write adapters, decoders and handlers for specific devices, data formats
  and databases.
