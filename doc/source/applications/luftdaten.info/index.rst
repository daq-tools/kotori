.. include:: ../../_resources.rst

.. _vendor-luftdaten.info:

##############
luftdaten.info
##############

.. contents::
   :local:
   :depth: 1

----



*****
About
*****
`luftdaten.info`_ is a community project from Stuttgart, Germany.
Due to its geographical location, they have high particulate matter (PM) levels on a regular basis.

People around the `OK Lab Stuttgart`_, a project supported by `code for germany`_
of the `open knowledge foundation`_ constructed cost-effective particulate sensors easily to rebuild by everyone.
The sensor readings are acquired by the backend application `feinstaub-api`_, displayed in `luftdaten.info map`_
and archived at `luftdaten.info Archive`_.

Luftdaten.info is in the process of installing low cost, crowdfunded sensor nodes across
many cities in Germany to measure PM levels.


****
Goal
****
The goal is to display data from luftdaten.info using a rich data visualization dashboard in Grafana_.
Historical data should be able to be displayed by geographical location to make it a meaningful supplement
to the `luftdaten.info map`_.
luftdaten.info already makes all historical data accessible on the `luftdaten.info Archive`_ (CSV format)
and live data via `luftdaten.info API`_ (JSON format).

There are two goals:

a) republish live JSON data to MQTT and
b) import historical CSV data


**********
Status quo
**********

LuftdatenPumpe
==============
The main workhorse, `luftdaten-to-mqtt`_ requests data from the live API of luftdaten.info each 10 minutes,
enriches it with geospatial information (reverse geocoding) and republishes its results to the MQTT bus.
From there, the regular data acquisition subsystem collects the measurement data, stores it into InfluxDB
appropriately and adds a rich data visualization dashboard to Grafana.

`luftdaten-to-mqtt`_ can be used as an universal MQTT forwarder, as `Rajko <https://github.com/ricki-z>`_
explains `here <https://github.com/opendata-stuttgart/sensors-software/issues/33#issuecomment-272711445>`_:

    | You can easily implement a "proxy" that translates json to mqtt. Then you can use this proxy as custom api.
    | Historical data can be found here: https://archive.luftdaten.info/
    | Graphs can be found here: https://www.madavi.de/sensor/graph.php
    | Live data can be found here: https://api.luftdaten.info/static/v1/data.json
    | This file is updated every minute and contains all sensors and values sent to the server in the last 5 minutes.

The setup is pretty straight-forward, see also :ref:`luftdaten.info-setup`.

.. todo::

    All acquisition infrastructure for importing **historical** data is in place already (see :ref:`daq-http-csv` import),
    but there is still some data munging required. To get results of similar richness as the live data import,
    some parts of the code should be refactored from the `luftdaten-to-mqtt`_ program to the internal data acquisition routines.


****
Demo
****
- https://luftdaten.getkotori.org/grafana/dashboard/db/luftdaten-tresholds
- https://luftdaten.getkotori.org/grafana/dashboard/db/luftdaten-map


*********
Live data
*********

.. raw:: html

    <iframe src="https://luftdaten.getkotori.org/grafana/dashboard-solo/db/luftdaten-tresholds?orgId=1&var-Location=Gr%C3%BCntaler%20Stra%C3%9Fe%2C%20Gesundbrunnen%2C%20Berlin%2C%20DE&panelId=18&theme=light" width="100%" height="600" frameborder="0"></iframe>


***********
Screenshots
***********

.. figure:: https://ptrace.isarengineering.de/2017-04-24_luftdaten-measurements-by-location.jpg
    :target: https://luftdaten.getkotori.org/grafana/dashboard/db/luftdaten-tresholds
    :alt: luftdaten.info - Measurements by location
    :width: 1024

    luftdaten.info - Measurements by location


.. figure:: https://ptrace.isarengineering.de/2017-04-24_luftdaten-location-chooser.jpg
    :alt: luftdaten.info - Location chooser
    :width: 1024

    luftdaten.info - Location chooser


.. figure:: https://ptrace.isarengineering.de/2017-04-24_luftdaten-grafana-worldmap.jpg
    :target: https://luftdaten.getkotori.org/grafana/dashboard/db/luftdaten-map
    :alt: luftdaten.info - Grafana Worldmap
    :width: 1024

    luftdaten.info - Grafana Worldmap


.. _luftdaten.info-setup:

*****
Setup
*****

InfluxDB
========
/etc/influxdb/influxdb.conf::

    [[udp]]
      # High-traffic UDP
      enabled = true
      bind-address = ":4445" # the bind address
      database = "luftdaten_testdrive" # Name of the database that will be written to
      batch-size = 5000 # will flush if this many points get buffered
      batch-timeout = "30s" # will flush at least this often even if the batch-size is not reached
      batch-pending = 100 # number of batches that may be pending in memory
      read-buffer = 8388608 # (8*1024*1024) UDP read buffer size

Kotori
======
Use https://github.com/daq-tools/kotori/blob/master/etc/examples/vendors/luftdaten.ini as configuration::

    ln -sr /etc/kotori/examples/vendors/luftdaten.ini /etc/kotori/apps-available/
    ln -sr /etc/kotori/apps-available/luftdaten.ini /etc/kotori/apps-enabled/
    systemctl restart kotori


LuftdatenPumpe
==============
`luftdaten-to-mqtt`_ requests data from the live API of luftdaten.info,
enriches it with geospatial information and republishes it to the MQTT bus.

Synopsis
--------
::

    /opt/kotori/bin/luftdaten-to-mqtt --mqtt-uri mqtt://mqtt.example.org/luftdaten/testdrive/earth/42/data.json --geohash --reverse-geocode --progress
    2017-04-22 03:55:50,426 [kotori.vendor.luftdaten.luftdaten_api_to_mqtt] INFO   : Publishing data to MQTT URI mqtt://mqtt.example.org/luftdaten/testdrive/earth/42/data.json
    2017-04-22 03:55:51,396 [kotori.vendor.luftdaten.luftdaten_api_to_mqtt] INFO   : Timestamp of first record: 2017-04-22T01:50:02Z
    100%|..........................................................................| 6782/6782 [01:01<00:00, 109.77it/s]

Run each 10 minutes
-------------------
/etc/cron.d/luftdaten-to-mqtt::

    # /etc/cron.d/luftdaten-to-mqtt -- forward data from luftdaten.info json api to mqtt

    # run luftdaten-to-mqtt each 10 minutes
    */10 * * * * root /opt/kotori/bin/luftdaten-to-mqtt --mqtt-uri mqtt://mqtt.example.org/luftdaten/testdrive/earth/42/data.json --geohash --reverse-geocode --progress


******
Agenda
******
There are more things on the todo list.

.. toctree::
    :maxdepth: 1
    :glob:

    agenda



.. _luftdaten.info: http://luftdaten.info
.. _luftdaten.info map: http://deutschland.maps.luftdaten.info/
.. _luftdaten.info Archive: http://archive.luftdaten.info
.. _OK Lab Stuttgart: https://codefor.de/stuttgart/
.. _code for germany: https://codefor.de/
.. _open knowledge foundation: https://okfn.de/
.. _Source - theguardian.com 2017: https://www.theguardian.com/cities/2017/mar/02/stuttgart-residents-sue-mayor-bodily-harm-air-pollution
.. _Kotori: https://getkotori.org
.. _luftdaten.info API: https://api.luftdaten.info/static/v1/data.json
.. _luftdaten-to-mqtt: https://github.com/daq-tools/kotori/blob/master/kotori/vendor/luftdaten/luftdaten_api_to_mqtt.py
.. _feinstaub-api: https://github.com/opendata-stuttgart/feinstaub-api

