=======================
Kotori DAQ Debian setup
=======================

System level packages
---------------------
::

    aptitude install python-virtualenv build-essential python-dev libffi-dev libssl-dev


InfluxDB
========
::

    wget https://s3.amazonaws.com/influxdb/influxdb_0.9.4.2_amd64.deb
    dpkg -i influxdb_0.9.4.2_amd64.deb

/etc/opt/influxdb/influxdb.conf::

    [meta]
      hostname = "elbanco.hiveeyes.org"

    [http]
      auth-enabled = true
      log-enabled = true

configure rsyslog::

    cat /etc/rsyslog.d/influxdb.conf
    # redirect to application log
    if $programname contains 'influxd' then /var/log/influxdb/influxd.log

    # prevent bubbling up into daemon.log
    if $programname contains 'influxd' then stop

restart rsyslog::

    service rsyslog restart

start influxdb::

    service influxdb start
    tail -F /var/log/influxdb/influxd.log


Grafana
=======
Install package::

    aptitude install apt-transport-https curl

    cat /etc/apt/sources.list.d/grafana.list
    deb https://packagecloud.io/grafana/stable/debian/ wheezy main

    curl https://packagecloud.io/gpg.key | apt-key add -
    aptitude update
    aptitude install grafana


Configure::

    /etc/grafana/grafana.ini
    admin_password = XYZ


Run::

    /etc/init.d/grafana-server start
    tail -F /var/log/grafana/grafana.log
