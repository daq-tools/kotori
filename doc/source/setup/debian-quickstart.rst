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

Access Grafana
==============

- Go to http://kotori.example.org:3000/
- Login with admin / admin.


Configure Kotori application
============================

- ::

    cp /etc/kotori/examples/mqttkit.ini /etc/kotori/apps-available/amazonas.ini

- Edit::

    realm       = amazonas
    mqtt_topics = amazonas/#

- Activate::

    ln -s /etc/kotori/apps-available/amazonas.ini /etc/kotori/apps-enabled/

- Watch Kotori logfile::

    tail -F /var/log/kotori/kotori.log

- Restart Kotori::

    systemctl restart kotori


Send sample telemetry packet
============================
::

    mosquitto_pub -t amazonas/ecuador/cuyabeno/1/message-json -m '{"temperature": 42.84, "humidity": 94}'


Watch telemetry data
====================
- Navigate to http://kotori.example.org:3000/dashboard/db/ecuador


***************
Troubleshooting
***************

No data in Grafana I
====================

- Q: I don't see any data

- A: Most probably, your system time is wrong or deviates from the time of the system accessing Grafana from.
  For example, you won't see any data if the server time is in the future.
  Suggestion: Better install ``chrony`` or use other means to keep your system times sound.


No data in Grafana II
=====================
- Q: I still don't see any data
- A: Try to increase the log level by adding ``--debug-foobar`` command line options to ``/etc/default/kotori``
  and get back to us, stacktrace or GTFO.
  See ``/opt/kotori/bin/kotori --help`` for available options.

Example ``/etc/default/kotori``::

    KOTORI_OPTS="--debug-mqtt --debug-influx"

