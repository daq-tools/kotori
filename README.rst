=============
Kotori README
=============

Kotori DAQ is a multi-channel, multi-protocol data acquisition and graphing toolkit based on InfluxDB_, Grafana_ and Twisted_.

It is a convenient component for building telemetry solutions and test benches. It addresses different aspects of collecting
and storing sensor data from a multitude of data sources. The framework design has two audiences in mind.


For users
---------
Interactively create data sinks, add decoding- and mapping-rules and finally store data points into InfluxDB_,
a leading open source time series database suitable for realtime analytics and sensor data storage.

Interactively build realtime dashboards to visualize time series data with Grafana_,
an open source, feature rich metrics dashboard and graph editor.


For developers
--------------
Ingest and distribute data between multiple publishers and subscribers across
different devices using the underpinning software bus based on
`The WebSocket Protocol`_ and `The Web Application Messaging Protocol`_.

Leverage the open infrastructure based on Twisted_ - an event-driven networking engine -
to implement custom software components.
Accept new protocols, write adapters, decoders and handlers for specific devices and data formats.



.. _InfluxDB: https://influxdb.com/
.. _Grafana: http://grafana.org/
.. _Twisted: https://twistedmatrix.com/
.. _The WebSocket Protocol: https://tools.ietf.org/html/rfc6455
.. _The Web Application Messaging Protocol: http://wamp.ws/
