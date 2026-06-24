.. include:: ../_resources.rst

.. _setup-debian:
.. _setup-debian-amd64:
.. _setup-debian-quickstart:

##########################
Setup on Debian and Ubuntu
##########################


*******
Preface
*******

This part of the documentation covers the installation of Kotori and the whole
software stack for telemetry data acquisition, processing and visualization on
Debian and Ubuntu systems.

The first step to using any software package is getting it properly installed.
Please read this section carefully.

After successfully installing the software, you might want to follow up with
its configuration at :ref:`getting-started`.


************
Introduction
************

The package repository provides packages for computers with x86-64 and ARM processors.


************
Installation
************

Prerequisites
=============

We are going to do telemetry data acquisition, sometimes coming from measurement
systems which **do not** send appropriate timestamps. Thus, the timekeeping
of your data acquisition system itself should be accurate.

So, either enable the NTP feature of ``systemd``::

    timedatectl set-ntp true

or install ``chrony``::

    apt install chrony

or implement any other valid equivalent to keep the system time sound.

For registering 3rd-party package repositories offering their packages
through https, please invoke the following commands::

    apt install apt-transport-https software-properties-common wget gnupg


Register the mosquitto package repository
=========================================
Add GPG key for checking package signatures::

    wget -qO - https://repo.mosquitto.org/debian/mosquitto-repo.gpg.key | apt-key add -

Add package source for either Debian 10.x buster or Ubuntu 18 Bionic Beaver::

    apt-add-repository 'deb https://repo.mosquitto.org/debian buster main'

or Debian 9.x stretch::

    apt-add-repository 'deb https://repo.mosquitto.org/debian stretch main'


Register the main package repository
====================================
Add GPG key for checking package signatures::

    wget -qO - https://packages.elmyra.de/elmyra/foss/debian/pubkey.txt | apt-key add -

Add package source for either Debian 10.x buster::

    apt-add-repository 'deb https://packages.elmyra.de/elmyra/foss/debian/ buster main foundation'

or Ubuntu 18 Bionic Beaver::

    apt-add-repository 'deb https://packages.elmyra.de/elmyra/foss/debian/ bionic main foundation'

or Debian 9.x stretch::

    apt-add-repository 'deb https://packages.elmyra.de/elmyra/foss/debian/ stretch main foundation'

Reindex package database::

    apt update


Setup the whole software stack
==============================
Install Kotori together with all recommended and suggested packages::

    apt install --install-recommends kotori

CrateDB, InfluxDB, and Grafana are not always enabled and started automatically,
so ensure they are running by invoking::

    systemctl enable mosquitto crate influxdb grafana-server
    systemctl start mosquitto crate influxdb grafana-server

Notes for ARM machines
======================
For using Kotori on ARM machines like the RaspberryPi or the BeagleBone SBCs,
there is a more lightweight package with fewer dependencies called
``kotori-standard``. To install it, invoke::

    apt install --install-recommends kotori-standard


**********
Operations
**********

Watching the system logs
========================

Being able to investigate problems is crucial. The first step is to inspect corresponding
log files. At a glance, those are the log files where system messages may appear, depending
on how you installed and run the corresponding services::

    tail -F /var/log/kotori/*.log /var/log/grafana/*.log /var/log/crate/*.log /var/log/influxdb/*.log /var/log/mosquitto/*.log

On modern Linux systems, log messages may be routed to systemd's journal daemon. In order to
inspect them, invoke, for example::

    journalctl -u kotori -u grafana -u crate -u influxdb -u mosquitto

