.. include:: ../_resources.rst

.. _systemd-development-mode:

###############################
Kotori development with systemd
###############################

.. contents:: Table of Contents
   :local:
   :depth: 2

----

Run as service
==============
You should go to the :ref:`setup-debian` packages.

When still having the desire to run the application
as system service while being in development mode,
read on.

We actively use this scenario for integration
scenarios and debugging.


general
-------
Let's add a user to the system and proceed as non-root::

    useradd --create-home --shell /bin/bash kotori
    su - kotori


systemd service
---------------

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

