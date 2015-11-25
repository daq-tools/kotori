.. _vendor-hydro2motion:

============
Hydro2Motion
============

.. contents:: Table of Contents
   :local:
   :depth: 2

Run Kotori
==========
::

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
