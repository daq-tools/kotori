.. include:: ../_resources.rst

.. _vendor-hiveeyes:

########
Hiveeyes
########


*****
About
*****
The `Hiveeyes project`_ conceives a data collection platform for
bee hive monitoring voluntarily operated by the beekeeper community.

Together with Mosquitto_, InfluxDB_, Grafana_, mqttwarn_ and BERadio_,
Kotori powers the :ref:`Hiveeyes system <hiveeyes:hiveeyes-system>`
on ``swarm.hiveeyes.org`` as a data collection hub for a Berlin-based
beekeeper collective.


***********
Environment
***********
Let's have a look at the environment:

- Arduino_ is a popular embedded computing platform used intensively here.
- Telemetry data is transmitted from sensor nodes over RFM69_/RFM95_ radio links.
- Telemetry data is forwarded and distributed over
  a wide area multi-tenancy communication bus based on MQTT_.


************
Sensor nodes
************

The :ref:`vendor-hiveeyes` project for collaborative beehive
monitoring uses two different kinds of sensor nodes.

- :ref:`hiveeyes-one` sensor nodes transmit data to a gateway using RF,
  the gateway receives and decodes telemetry data from Bencode_ format,
  then forwards it to the MQTT_ broker in JSON.
  This is specified in :ref:`beradio-spec` and implemented
  in Python using the serial-to-mqtt forwarder :ref:`beradio-python <beradio-python>`.

- :ref:`open-hive` sensor nodes based on the *Adafruit HUZZAH ESP8266*
  directly send telemetry data to the MQTT_ broker in JSON format.


***************
System overview
***************


Radio link
==========
:ref:`beradio:beradio` handles the radio link communication based on RFM69_ and RFM95_.
It receives data messages in Bencode_ format over radio, decodes them and
forwards them to a serial interface to MQTT encoded with JSON.

.. graphviz:: hiveeyes/radio.dot


MQTT- and HTTP-based data acquisition, storage and visualization
================================================================
- :ref:`kotori` receives telemetry data from MQTT topic subscriptions.
  For details about the addressing scheme and topology, see :ref:`hiveeyes-one-topology`.
- The :ref:`Open Hive Box <openhive-box>` uses a GPRSbee modem to do :ref:`daq-http`.
- Store measurements to the timeseries database.
- Automatically create default Grafana panels for instant telemetry data visualization.
- Detect events and anomalies on the telemetry data and emit appropriate signals.

.. graphviz:: hiveeyes/acquisition.dot


Data export
===========
There are different ways to get data out of Kotori, see :ref:`data-export`.

.. graphviz:: hiveeyes/export.dot


Firmware builder
================
Using the :ref:`firmware-builder`, beekeepers can upload customized firmwares to
their sensor and telemetry nodes derived from a "golden master" :ref:`generic-firmware`.
Firmware images can be easily downloaded using HTTP.

.. graphviz:: hiveeyes/firmware.dot


Domain-specific features
========================
- Hiveeyes Daily
- Schwarmalarm
- Elektronische Stockkarte


*******
Results
*******

Intro
=====
Data currently is measured at intervals of about 15 minutes.

In the following graphs the weight of the hive is shown with the light blue line.
The temperature sensor inside the hive is shown in dark blue and
the sensor at the air hole, which is in the sun most times, is yellow.

Spring 2016
===========

.. raw:: html

    <iframe src="https://swarm.hiveeyes.org/grafana/dashboard-solo/db/hiveeyes-labs-wedding?panelId=5&from=20160418T200000&to=20160518T160000" width="100%" height="425" frameborder="0"></iframe>

.. container::

    Let's have a look at the data. During the cold period at the end of April the beehive loses absolute weight
    because the bees have to live on their reserves. In contrast, the following two weeks were amazingly warm in May,
    so the worker bees are getting extremely busy.

    From April 29 until May 13, the weight has increased by almost 14 Kg.
    On some days the beehive gained 2 Kg weigth due to pollen and nectar collecting.

    It was the time of the fruit blossoms, so the cherry, pear and apple trees were in bloom in the nearby allotments.


----

.. raw:: html

    <iframe src="https://swarm.hiveeyes.org/grafana/dashboard-solo/db/hiveeyes-labs-wedding?panelId=5&from=20160430T130000&to=20160503T040000" width="100%" height="425" frameborder="0"></iframe>

.. container::

    The beehive gained a lot of weight on the 2nd of May. After six o'clock in the morning
    the temperature begins to rise, at 7:15 the first sun rays shine on the entrance hole.
    The first scouts leave the beehive at 7:45 and at 8:15 everyone is in the air.
    The beehive suddenly loses 120g since about 1200 bees are leaving to harvest.

    At 9:20, the ratio between the arriving and departing bees reverses and the weight increases rapidly.

    Throughout the day, bees are flying in and out, collecting nectar and pollen, explore and report.
    Even as the beehive is in the shadow from 16:00 and the temperature starts sinking,
    the bee colony continues to collect until 20:00.

    1800g have been carried home. It was a good warm and important day,
    after the long period of winter and the cold snap at the end of April.

|clearfix|


Schwarmalarm May 2016
=====================

.. raw:: html

    <iframe src="https://swarm.hiveeyes.org/grafana/dashboard-solo/db/hiveeyes-labs-wedding?panelId=5&from=20160519T040000&to=20160519T170000" width="100%" height="425" frameborder="0"></iframe>

.. container::

    This is a weight-loss event from :ref:`hiveeyes-scale-beutenkarl`
    recorded on 2016-05-20 between 10:11 and 10:26 hours CEST after a
    bee colony started swarming at the Hiveeyes Labs Beehive in Berlin Wedding,
    see also :ref:`hiveeyes-schwarmalarm-2016-05-20`.

|clearfix|


*******
Details
*******

Interfaces
==========
Entrypoints to the platform running on ``swarm.hiveeyes.org`` as of 2016-01-29:

- MQTT: ``mqtt://swarm.hiveeyes.org``
- HTTP: ``https://swarm.hiveeyes.org/api``
- Grafana: ``https://swarm.hiveeyes.org/grafana/``


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

    The source code of the Hiveeyes project is available at `Hiveeyes at GitHub`_.


Under the hood
==============
Please also have a look at :ref:`hiveeyes-one-topology` and :ref:`hiveeyes-one-wishlist`.

