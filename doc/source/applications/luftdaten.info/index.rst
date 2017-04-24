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
and archived at `luftdaten.info archive`_.

Luftdaten.info is in the process of installing low cost, crowdfunded sensor nodes across
many cities in Germany to measure PM levels.


****
Goal
****
The `luftdaten.info map`_ lacks the historical comparable data but luftdaten.info makes
all data accessible via their `luftdaten.info archive`_ in *csv* format and live data
via `luftdaten.info json api`_.

We want to a) republish the live data to mqtt and b) import historical CSV data
to display both using Grafana_.


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
`luftdaten_api_to_mqtt`_ requests data from live API of luftdaten.info,
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
There are more things on our todo list.

.. toctree::
    :maxdepth: 1
    :glob:

    agenda



.. _luftdaten.info: http://luftdaten.info
.. _luftdaten.info map: http://deutschland.maps.luftdaten.info/
.. _luftdaten.info archive: http://archive.luftdaten.info
.. _OK Lab Stuttgart: https://codefor.de/stuttgart/
.. _code for germany: https://codefor.de/
.. _open knowledge foundation: https://okfn.de/
.. _Source - theguardian.com 2017: https://www.theguardian.com/cities/2017/mar/02/stuttgart-residents-sue-mayor-bodily-harm-air-pollution
.. _Kotori: https://getkotori.org
.. _luftdaten.info json api: https://api.luftdaten.info/static/v1/data.json
.. _luftdaten_api_to_mqtt: https://github.com/daq-tools/kotori/blob/master/kotori/vendor/luftdaten/luftdaten_api_to_mqtt.py
.. _feinstaub-api: https://github.com/opendata-stuttgart/feinstaub-api

