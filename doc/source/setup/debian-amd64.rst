.. include:: ../_resources.rst

.. _setup-debian:
.. _setup-debian-amd64:

############
Debian AMD64
############

.. contents:: Table of Contents
   :local:
   :depth: 2

----

*****
Intro
*****
Install the whole stack on a Debian-based system. It is currently made of:

- Mosquitto_, an open source MQTT message broker
- InfluxDB_, an open source time-series database
- Grafana_, a graph and dashboard builder for visualizing time series metrics
- Kotori_, a data acquisition and graphing toolkit acting as a mediator


**************
Infrastructure
**************

Mosquitto
=========
::

    aptitude install mosquitto mosquitto-clients


InfluxDB
========
::

    wget https://s3.amazonaws.com/influxdb/influxdb_0.10.0-0.beta2_amd64.deb
    dpkg -i influxdb_0.10.0-0.beta2_amd64.deb


Alternatives (don't use the 0.8.x releases):

    - https://s3.amazonaws.com/influxdb/influxdb_0.10.0-0.beta2_amd64.deb
    - https://s3.amazonaws.com/influxdb/influxdb_0.9.6.1_amd64.deb
    - https://s3.amazonaws.com/influxdb/influxdb_0.9.4.2_amd64.deb
    - https://s3.amazonaws.com/influxdb/influxdb_0.8.8_amd64.deb


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

    aptitude install apt-transport-https curl
    curl https://packagecloud.io/gpg.key | apt-key add -
    echo 'deb https://packagecloud.io/grafana/stable/debian/ wheezy main' > /etc/apt/sources.list.d/grafana.list

    aptitude update
    aptitude install grafana


Configure::

    /etc/grafana/grafana.ini
    admin_password = XYZ


Run::

    #/etc/init.d/grafana-server start
    systemctl enable grafana-server
    systemctl start grafana-server
    tail -F /var/log/grafana/grafana.log



******
Kotori
******


Kotori Debian package
=====================
We don't have a solid Debian repository as of 2016-01-29 yet, but at least we have any packages::

    wget https://packages.elmyra.de/hiveeyes/debian/kotori_0.6.0-1_amd64.deb
    dpkg --install kotori_0.6.0-1_amd64.deb
    tail -F /var/log/kotori/*.log

When adjusting the configuration in ``/etc/kotori/kotori.ini``, please restart the service::

    systemctl restart kotori

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

