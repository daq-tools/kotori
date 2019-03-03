.. include:: ../_resources.rst

.. _setup-debian:
.. _setup-debian-quickstart:

###############
Setup on Debian
###############

.. contents::
   :local:
   :depth: 1

----


************
Introduction
************
This part of the documentation covers the installation of Kotori and other
software components it relies on.
The first step to using any software package is getting it properly installed.
Please read this section carefully.
After successfully installing the software, you might want to
follow up with its configuration at :ref:`getting-started`.


Details
=======
This document describes the installation of the whole software stack for
telemetry data acquisition, processing and visualization on a Debian-based
system. It is currently made of these free and open source software components:

- :ref:`Kotori`, a data acquisition, graphing and telemetry toolkit
- Grafana_, a graph and dashboard builder for visualizing time series metrics
- InfluxDB_, a time-series database
- Mosquitto_, a MQTT message broker
- MongoDB_, a document store (optional) ¹²

The package repository supports both architectures ``amd64`` and ``armhf`` (arm32v7).

| ¹ MongoDB is only required when doing CSV data acquisition, so it is completely
| optional for regular operations of Kotori.
| ² As MongoDB - strictly speaking - stopped being free software recently (2018/2019),
| it will probably be phased out gradually and replaced by PostgreSQL.


Outlook
=======
Some effort has been done to make the installation process of Kotori and
associated software components as easy and straight forward as possible.

However, things are complicated sometimes so there might still be rough
edges we would love to learn about. So, don't hesitate to drop us a note
by `opening an issue on GitHub <https://github.com/daq-tools/kotori/issues/new>`_
or reaching out to ``support@getkotori.org``. Thanks already.


************
Installation
************

Prerequisites
=============
We are going to do telemetry data acquisition, sometimes coming from measurement
systems which **do not** send appropriate timestamps. Thus, the timekeeping
of your data acquisition system itself should be accurate.

So, you either might want to enable the NTP feature of ``systemd``::

    timedatectl set-ntp true

or install ``chrony``::

    apt install chrony

or implement any other valid equivalent to keep the system time sound.

Register with package repository
================================
Add https addon for apt::

    apt install apt-transport-https software-properties-common

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

Don't be afraid of the command here, it's just for making sure all dependencies get satisfied.

Maybe it's already that easy now?::

    apt install --install-recommends --install-suggests kotori

InfluxDB and Grafana are not always started automatically, so ensure they are running by executing::

    systemctl start influxdb grafana-server


*********
Operation
*********

Watching the system
===================
These are the log files at a glance where system messages might appear::

    tail -F /var/log/kotori/*.log /var/log/grafana/*.log /var/log/influxdb/*.log /var/log/mosquitto/*.log
    journalctl -f -u influxdb


*************
Configuration
*************
Follow along at :ref:`getting-started` to configure and use your first Kotori application.

----

Have fun and enjoy your data acquisition!
