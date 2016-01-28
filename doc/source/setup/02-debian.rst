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

=========
Mosquitto
=========
::

    aptitude install mosquitto mosquitto-clients


========
InfluxDB
========
::

    wget https://s3.amazonaws.com/influxdb/influxdb_0.10.0-0.beta2_amd64.deb
    dpkg -i influxdb_0.10.0-0.beta2_amd64.deb


Alternatives:

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


=======
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

===============
System packages
===============
::

    aptitude install python-virtualenv build-essential python-dev libffi-dev libssl-dev


============
Manual setup
============

General
-------
Let's add a user to the system::

    useradd --create-home --shell /bin/bash kotori
    su - kotori


Install from Python Egg
-----------------------
Into virtualenv::

    mkdir -p ~/develop/kotori
    virtualenv ~/develop/kotori/.venv27
    ~/develop/kotori/.venv27/bin/pip install kotori[daq] \
        --extra-index-url=https://packages.elmyra.de/isarengineering/python/eggs/ \
        --upgrade

Into system::

    aptitude install python-pip
    pip install kotori[daq] \
        --extra-index-url=https://packages.elmyra.de/isarengineering/python/eggs/ \
        --upgrade

Add ``/etc/kotori/kotori.ini``:

.. literalinclude:: ../_static/content/hiveeyes.ini
    :language: ini



Install from git
----------------
::

    mkdir develop
    git clone git@git.elmyra.de:isarengineering/kotori.git ~/develop/kotori
    cd develop/kotori
    virtualenv .venv27
    source .venv27/bin/activate
    python setup.py develop

.. note:: Please contact us for repository access until the source code is on GitHub.


Run ad hoc
----------
::

    ~/develop/kotori/.venv27/bin/kotori --config ~/develop/kotori/etc/development.ini --debug

.. note::

    An alternative way to specify the configuration file::

        export KOTORI_CONFIG=/etc/kotori/kotori.ini

        kotori


Run as service
--------------

Configure as systemd service:

1. The systemd startup script expects the ``kotori`` executable to be at ``/usr/local/sbin/kotori``
   and its configuration file at ``/etc/kotori/kotori.ini``::

    mkdir -p /etc/kotori
    chown kotori:kotori /etc/kotori
    ln -s /home/kotori/develop/kotori/.venv27/bin/kotori /usr/local/sbin/kotori
    ln -s /home/kotori/develop/kotori/etc/hiveeyes.ini /etc/kotori/kotori.ini

2. Create the log directory::

    mkdir /var/log/kotori
    chown kotori:kotori /var/log/kotori

3. Copy the systemd script ``kotori.service`` into the system::

     cp /home/kotori/develop/kotori/packaging/systemd/kotori.service /usr/lib/systemd/system/

   Amend ``/usr/lib/systemd/system/kotori.service`` and adapt path to executable to ``/usr/local/sbin/kotori`` in ExecStart

.. attention:: Symlinking does not work in any case! See also:

    | systemctl enable fails for symlinks in /etc/systemd/system
    | https://bugzilla.redhat.com/show_bug.cgi?id=955379

4. Add yet another file ``/etc/default/kotori``::

    KOTORI_OPTS="--debug"

5. Profit::

    systemctl enable kotori
    systemctl start kotori

6. Check::

    root@elbanco:~# systemctl status kotori
    ● kotori.service - Kotori data acquisition and graphing toolkit
       Loaded: loaded (/usr/lib/systemd/system/kotori.service; enabled)
       Active: active (running) since Wed 2016-01-27 03:47:05 CET; 1h 4min ago
         Docs: http://isarengineering.de/docs/kotori/
     Main PID: 345 (sh)
       CGroup: /system.slice/kotori.service
               ├─345 /bin/sh -c /usr/local/sbin/kotori --config /etc/kotori/kotori.ini --debug >>/var/log/kotori/kotori.log 2>>/var/log/kotor...
               └─355 /home/kotori/develop/kotori-daq/.venv27/bin/python /usr/local/sbin/kotori --config /etc/kotori/kotori.ini --debug

    Jan 27 03:47:05 elbanco systemd[1]: Started Kotori data acquisition and graphing toolkit.

7. Watch::

    tail -F /var/log/kotori/kotori.log

    2016-01-27T03:17:57+0100 [kotori                            ] INFO: Kotori version 0.5.1
    2016-01-27T03:17:57+0100 [kotori.vendor.hiveeyes.application] INFO: Starting HiveeyesApplication
    2016-01-27T03:17:57+0100 [kotori.daq.graphing.grafana       ] INFO: Starting GrafanaManager "HiveeyesGrafanaManager". grafana=localhost:3000
    2016-01-27T03:17:57+0100 [kotori.daq.intercom.mqtt_adapter  ] INFO: Starting MQTTAdapter. broker=localhost:1883
    2016-01-27T03:17:57+0100 [mqtt.client.factory               ] INFO: MQTT Client library version 0.1.2
    2016-01-27T03:17:57+0100 [mqtt.client.factory.MQTTFactory   ] INFO: Starting factory <mqtt.client.factory.MQTTFactory instance at 0x7f745c54aa28>
    2016-01-27T03:17:57+0100 [mqtt.client.base                  ] DEBUG: ==> CONNECT (id=kotori.mqtt keepalive=0 clean=True)
    2016-01-27T03:17:57+0100 [mqtt.client.base                  ] DEBUG: <== CONNACK (code=0 session=False)


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

