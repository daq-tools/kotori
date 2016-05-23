.. include:: ../_resources.rst

.. _setup-debian:
.. _setup-debian-quickstart:

###############
Setup on Debian
###############

.. contents::
   :local:
   :depth: 2

----

*****
Intro
*****
Install the whole stack on a Debian-based system.
The package repository supports architectures amd64 and armhf as of 2016-05-23.

It is currently made of these free and open source software components:

- Grafana_, a graph and dashboard builder for visualizing time series metrics
- InfluxDB_, a time-series database
- Mosquitto_, a MQTT message broker
- :ref:`Kotori`, a data acquisition, graphing and telemetry toolkit



***********
Setup steps
***********

Prerequisites
=============

Add GPG key for checking package signatures::

    wget -qO - https://packages.elmyra.de/elmyra/foss/debian/pubkey.txt | apt-key add -

Add https addon for apt::

    aptitude install apt-transport-https


Register with package repository
================================

Add source for "testing" distribution (e.g. append to /etc/apt/sources.list)::

    deb https://packages.elmyra.de/elmyra/foss/debian/ testing main foundation

Reindex package database::

    aptitude update


Setup the whole software stack
==============================
::

    aptitude install chrony mosquitto mosquitto-clients influxdb grafana kotori
    systemctl start influxdb


***************
Getting started
***************
Follow along at :ref:`getting-started` to configure and use your first Kotori application.
