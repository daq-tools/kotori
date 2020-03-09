.. include:: ../../_resources.rst

############
Debian AMD64
############

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


**************
Infrastructure
**************

Mosquitto
=========
::

    wget --quiet -O - http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key | apt-key add -
    echo 'deb http://repo.mosquitto.org/debian stretch main' > /etc/apt/sources.list.d/mosquitto.list
    apt update

::

    apt install mosquitto mosquitto-clients


InfluxDB
========
::

    wget https://s3.amazonaws.com/influxdb/influxdb_0.12.2-1_amd64.deb
    dpkg --install influxdb_0.10.2-1_amd64.deb

/etc/influxdb/influxdb.conf::

    [http]
      auth-enabled = true
      log-enabled = true

Configure rsyslog::

    cat /etc/rsyslog.d/influxdb.conf
    # redirect to application log
    if $programname contains 'influxd' then /var/log/influxdb/influxd.log

    # prevent bubbling up into daemon.log
    if $programname contains 'influxd' then stop

Restart rsyslog::

    service rsyslog restart

Start InfluxDB daemon::

    systemctl start influxdb
    tail -F /var/log/influxdb/influxd.log


Grafana
=======
Install package::

    apt install apt-transport-https curl
    curl https://packagecloud.io/gpg.key | apt-key add -
    echo 'deb https://packagecloud.io/grafana/stable/debian/ wheezy main' > /etc/apt/sources.list.d/grafana.list

    apt update
    apt install grafana


Configure::

    /etc/grafana/grafana.ini
    admin_password = XYZ


Enable system service::

    systemctl enable grafana-server
    systemctl is-enabled grafana-server

Start system service::

    systemctl start grafana-server
    tail -F /var/log/grafana/grafana.log


******
Kotori
******

Kotori package
==============

Prerequisites
-------------

Add GPG key for checking package signatures::

    wget -qO - https://packages.elmyra.de/elmyra/foss/debian/pubkey.txt | apt-key add -

Add https addon for apt::

    apt install apt-transport-https


Register with package repository
--------------------------------

Add package source for Debian stretch::

    deb https://packages.elmyra.de/elmyra/foss/debian/ stretch main

Add package source for Debian buster::

    deb https://packages.elmyra.de/elmyra/foss/debian/ buster main

Reindex package database::

    apt update


Install package
---------------
::

    apt install kotori


.. seealso:: https://packages.elmyra.de/elmyra/foss/debian/README.txt

When adjusting the configuration in ``/etc/kotori``, please restart the service::

    systemctl restart kotori
    tail -F /var/log/kotori/*.log

For information beyond the package level, please visit :ref:`kotori-hacking`.


Daemon control
==============
Business as usual::

    systemctl start|stop|restart|status kotori
    systemctl enable|disable kotori


****************
All together now
****************

Check the status of all services::

    systemctl list-units influxdb* mosquitto.service grafana-server* kotori*
    systemctl status     influxdb* mosquitto.service grafana-server* kotori*


Count them::

    systemctl list-units influxdb* mosquitto.service grafana-server* kotori* | grep running | wc -l
    4

Watch the logs::

    tail -F /var/log/syslog /var/log/influxdb/*.log /var/log/mosquitto/* /var/log/grafana/*.log /var/log/kotori/*.log

