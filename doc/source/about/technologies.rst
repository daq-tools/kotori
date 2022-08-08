.. include:: ../_resources.rst


.. _kotori-technologies:

############
Technologies
############


************
Introduction
************

The system is based on a number of fine infrastructure components and
technologies and supports a number of protocols in one way or another.
Standing on the shoulders of giants.


*******
Details
*******

Infrastructure components
=========================

- Kotori_, a data acquisition, graphing and telemetry toolkit
- Grafana_, a graph and dashboard builder for visualizing time series metrics
- InfluxDB_, a time-series database
- Mosquitto_, an MQTT message broker
- MongoDB_, a document store (optional) ¹²

| ¹ MongoDB is only required when doing CSV data acquisition, so it is completely
| optional for regular operations of Kotori.
| ² As MongoDB - strictly speaking - stopped being free software recently (2018/2019),
| it will probably be phased out gradually and replaced by PostgreSQL_.


Supported protocols
===================

- MQTT_, a lightweight, publish-subscribe, machine to machine network protocol.
- HTTP_, the ubiquitous application layer protocol for distributed, collaborative, hypermedia information systems.
- WebSocket_, a computer communications protocol, providing full-duplex communication channels over a single TCP connection.
- WAMP_, a WebSocket subprotocol offering routed RPC and PubSub.
- Socket-based TCP_, UDP_.


Runtime components
==================

- Twisted_, an event-driven network programming framework
- Autobahn_, open-source implementations of the Web Application Messaging Protocol (WAMP_)
