.. include:: ../_resources.rst

.. _vendor-hiveeyes:

########
Hiveeyes
########

.. contents::
   :local:
   :depth: 1

----

*****
About
*****
The `Hiveeyes project`_ conceives a data collection platform for
bee hive monitoring voluntarily operated by the beekeeper community.

Together with Mosquitto_, InfluxDB_, Grafana_, mqttwarn_ and BERadio_,
Kotori runs the `Hiveeyes platform`_ ``swarm.hiveeyes.org`` as
a data collection hub for a Berlin-based beekeeper collective.
For documentation and pictures, have a look at :ref:`hiveeyes:hiveeyes`.

Feel welcome to join them, just drop an email at "hiveeyes-devs ät ideensyndikat.org".
They are friendly, we know them.



***********
Environment
***********
Let's have a look at the environment:

- Arduino_ is a popular embedded computing platform used intensively here.
- Telemetry data is transmitted from sensor nodes over RFM69_ radio links.
- Telemetry data is forwarded and distributed over
  a wide area multi-tenancy communication bus based on MQTT_.


*****
Goals
*****
- :ref:`beradio:beradio` handles the radio link communication based on RFM69_.
  It receives data messages in Bencode_ format over radio, decodes them and
  forwards them to a serial interface to MQTT encoded with JSON.
- :ref:`kotori` receives telemetry data from MQTT topic subscriptions.
  For details about the addressing scheme and topology, see :ref:`hiveeyes-one-topology`.
- Store measurements to the database.
- Automatically create default Grafana panels for instant telemetry data visualization.


*******
Details
*******

Interfaces
==========
Entrypoints to the platform running on ``swarm.hiveeyes.org`` as of 2016-01-29:

- Mosquitto::

    uri:      mqtt://swarm.hiveeyes.org

- Grafana::

    uri:      https://swarm.hiveeyes.org/grafana/
    username: hiveeyes
    password: Efocmunk



*******************
Platform operations
*******************
This section is about running the whole platform on your own hardware.
Please be aware this is a work in progress. We are happy to receive
valuable feedback for improving things gradually.

Install the platform
====================
The most convenient way is by using Debian packages for all
infrastructure services and Kotori, see :ref:`setup-debian`.
After that, the service should have been automatically started
by systemd so the system is ready to serve requests.

InfluxDB
========
For working directly with the InfluxDB_ API, please have a look at the :ref:`influxdb-handbook`.




********************
Platform development
********************

Want to dig even deeper? Read on my dear.

Setup
=====
When developing on Kotori or for ad-hoc installations, you should follow the
instructions for :ref:`installing Kotori as Python package <setup-python-package>`.

Run Kotori
==========
In ad-hoc installations, or when turning off the systemd service,
you might want to start Kotori interactively in the foreground::

    /opt/kotori/bin/kotori --config /etc/kotori/kotori.ini --debug

Hacking
=======
For getting your development sandbox up and running,
please have a look at :ref:`kotori-hacking`.

.. note::

    We are working on bringing the source code to `Hiveeyes at GitHub`_.
    Please don't hesitate to contact us by email at "hiveeyes-devs ät ideensyndikat.org"
    for source code access in the meanwhile.


Under the hood
==============
Please also have a look at :ref:`hiveeyes-one-topology` and :ref:`hiveeyes-one-wishlist`.
