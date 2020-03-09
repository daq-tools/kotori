.. include:: ../_resources.rst

.. _setup-arch-linux:

###################
Setup on Arch Linux
###################


*****
Intro
*****
Install the whole stack on an Arch Linux-based system.
The package repository supports architectures amd64 and armhf as of 2016-05-23.

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
::

    # TODO: Check the package names
    yaourt influxdb mongodb grafana mosquitto mosquitto-clients

.. seealso::

    - https://aur.archlinux.org/packages/influxdb/
    - https://www.archlinux.org/packages/mongodb
    - https://www.archlinux.org/packages/grafana
    - https://www.archlinux.org/packages/mosquitto


Kotori
======
::

    # Install "dpkg" package manager
    yaourt dpkg

    # Download amd64 package
    wget https://packages.elmyra.de/elmyra/foss/debian/pool/main/k/kotori/kotori_0.15.0-1_amd64.deb

    # Download armhf package
    wget https://packages.elmyra.de/elmyra/foss/debian/pool/main/k/kotori/kotori_0.15.0-1_armhf.deb

    # Setup package
    dpkg -i kotori_*.deb


.. note::

    Check for recent versions at https://packages.elmyra.de/elmyra/foss/debian/pool/main/k/kotori/,
    we also have packages for other architectures (e.g. armhf for RaspberryPi).



***************
Getting started
***************
Follow along at :ref:`getting-started` to configure and use your first Kotori application.

