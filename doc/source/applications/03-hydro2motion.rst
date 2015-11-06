=========================
Kotori for Hydro 2 Motion
=========================

Run Kotori
==========
::

    kotori --config=etc/hydro2motion.ini


Receive telemetry data
----------------------
- Open Browser at http://localhost:35000/


Send telemetry data
-------------------
- Run::

    h2m-udp-client "24000;15718;75813;1756;15253;229;220;204;811;1769;0;0;0;0;0;1;0;12;0;0;0;-18;0;4011;417633984;85402624;472851424;0;12242;43;42;0;0"


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
