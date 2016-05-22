.. include:: ../_resources.rst

.. _setup-debian:
.. _setup-debian-quickstart:

#################
Debian Quickstart
#################

.. contents::
   :local:
   :depth: 2

----

*****
Intro
*****
Install the whole stack on a Debian-based system. It is currently made of these free and open source software components:

- Mosquitto_, a MQTT message broker
- InfluxDB_, a time-series database
- Grafana_, a graph and dashboard builder for visualizing time series metrics
- :ref:`Kotori`, a data acquisition, graphing and telemetry toolkit


*****
Steps
*****

Prerequisites
-------------

Add GPG key for checking package signatures::

    wget -qO - https://packages.elmyra.de/elmyra/foss/debian/pubkey.txt | apt-key add -

Add https addon for apt::

    aptitude install apt-transport-https


Register with package repository
--------------------------------

Add source for "testing" distribution (e.g. append to /etc/apt/sources.list)::

    deb https://packages.elmyra.de/elmyra/foss/debian/ testing main foundation

Reindex package database::

    aptitude update


Setup the whole software stack
------------------------------
::

    aptitude install mosquitto mosquitto-clients influxdb grafana kotori
    systemctl start influxdb

