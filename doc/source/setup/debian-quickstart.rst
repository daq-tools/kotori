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
- :ref:`Kotori`, a data acquisition, graphing and telemetry toolkit



***********
Setup steps
***********

Prerequisites
=============

Add https addon for apt::

    apt install apt-transport-https software-properties-common


Register with package repository
================================

Add source for "testing" distribution (will append to /etc/apt/sources.list)::

    apt-add-repository 'deb https://packages.elmyra.de/elmyra/foss/debian/ testing main foundation'

Add GPG key for checking package signatures::

    wget -qO - https://packages.elmyra.de/elmyra/foss/debian/pubkey.txt | apt-key add -

Reindex package database::

    apt update


Setup the whole software stack
==============================
Install Kotori as well as recommended and suggested packages::

    PACKAGES=kotori
    DEPENDENCIES=$(LANG=c apt-cache depends $PACKAGES | egrep -i 'suggests|recommends' | grep -v '<' | cut -d' ' -f4 | xargs)
    apt install $PACKAGES $DEPENDENCIES
    systemctl start influxdb grafana-server

.. tip::

    You should keep your system time sound. Either carry out::

        timedatectl set-ntp true

    or install ``chrony``::

        apt install chrony



tail -F /var/log/kotori/*.log /var/log/grafana/*.log /var/log/influxdb/*.log /var/log/mosquitto/*.log
journalctl -f -u influxdb


***************
Getting started
***************
Follow along at :ref:`getting-started` to configure and use your first Kotori application.

