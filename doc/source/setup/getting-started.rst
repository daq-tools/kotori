.. include:: ../_resources.rst

.. _getting-started:

###############
Getting started
###############
.. highlight:: bash

.. contents::
   :local:
   :depth: 2

----

.. todo::

    - Swap content from here with :ref:`kotori-handbook`
    - Rename this file to "setup/kotori.rst".
    - How to bring :ref:`application-mqttkit` into the mix?


*****
Intro
*****
Configure an example application with Kotori based on the :ref:`application-mqttkit` communication style.


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

    mosquitto_pub -t amazonas/ecuador/cuyabeno/1/data.json -m '{"temperature": 42.84, "humidity": 94}'


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

    .. tip::

        Better install ``chrony`` or use other means to keep your system times sound::

            aptitude install chrony


No data in Grafana II
=====================
- Q: I still don't see any data
- A: Try to increase the log level by adding ``--debug-foobar`` command line options to ``/etc/default/kotori``
  and get back to us, stacktrace or GTFO.
  See ``/opt/kotori/bin/kotori --help`` for available options.

Example ``/etc/default/kotori``::

    KOTORI_OPTS="--debug-mqtt --debug-influx"

