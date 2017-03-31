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
The package repository supports architectures amd64 and armhf as of May 23, 2016.

It is currently made of these free and open source software components:

- InfluxDB_, a time-series database
- MongoDB_, a document store (optionally)
- Grafana_, a graph and dashboard builder for visualizing time series metrics
- Mosquitto_, a MQTT message broker
- Kotori_, a data acquisition, graphing and telemetry toolkit



***********
Setup steps
***********

Prerequisites
=============

Add GPG key for checking package signatures::

    wget -qO - https://packages.elmyra.de/elmyra/foss/debian/pubkey.txt | apt-key add -

Add https addon for apt::

    apt-get install apt-transport-https


Register with package repository
================================

Add source for "testing" distribution (e.g. append to /etc/apt/sources.list)::

    deb https://packages.elmyra.de/elmyra/foss/debian/ testing main foundation

Reindex package database::

    apt-get update


Setup the whole software stack
==============================
Install Kotori as well as recommended and suggested packages::

    PACKAGES=kotori
    DEPENDENCIES=$(LANG=c apt-cache depends $PACKAGES | egrep -i 'suggests|recommends' | cut -d' ' -f4 | xargs)
    apt-get install $PACKAGES $DEPENDENCIES
    systemctl start influxdb

.. tip::

    Better install ``chrony`` or use other means to keep your system times sound::

        aptitude install chrony


***************
Getting started
***************
Follow along at :ref:`getting-started` to configure and use your first Kotori application.

