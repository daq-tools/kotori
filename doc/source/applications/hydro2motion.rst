.. include:: ../_resources.rst

.. _vendor-hydro2motion:

============
Hydro2Motion
============

.. contents:: Table of Contents
   :local:
   :depth: 1


*****
About
*****
Kotori was running the telemetry platform for the Hydro2Motion_ team
at the "`Shell Eco-marathon`_ 2015" in Rotterdam.
This is a fine project out of the `Labor für Systemtechnik`_
at the `Munich University of Applied Sciences`_.

While this communication layer was based on CSV-over-UDP,
the next iteration of the communication layer is based
on Binary-over-UDP. This transport communicates more
efficiently while still retaining a maximum of convenience.
See also the :ref:`data acquisition system for vendor "LST" <vendor-lst>`.


*******
Details
*******

.. attention::

    This section is just a stub. Read the source, luke.


Run Kotori
==========
Crossbar router::

    crossbar start

Main application::

    kotori --config=etc/hydro2motion.ini


Receive telemetry data
----------------------
- Open Browser at http://localhost:35000/


Send telemetry data
-------------------
- Fixed data::

    h2m-csv-udp-client "24000;15718;75813;1756;15253;229;220;204;811;1769;0;0;0;0;0;1;0;12;0;0;0;-18;0;4011;417633984;85402624;472851424;0;12242;43;42;0;0"

- Random data::

    h2m-csv-udp-fuzzer

- Continuously send random data::

    watch -n0.5 h2m-csv-udp-fuzzer


URL entrypoints
===============

GUI
---
- | Kotori Telemetry Dashboard for Hydro2Motion
  | http://lablab.cicer.de:35000/
  | http://h2mdata.cicer.de/

Components
----------
- | InfluxDB UI
  | http://lablab.cicer.de:8083/
- | InfluxDB API
  | http://lablab.cicer.de:8086/
- | Grafana
  | http://lablab.cicer.de:3000/


Query InfluxDB
==============
::

    $ export INFLUX_URI=http://localhost:8086/query?pretty=true
    $ curl --silent --get $INFLUX_URI --user admin:admin --data-urlencode 'db=hydro2motion' --data-urlencode 'q=select * from "telemetry";' | jq '.'

