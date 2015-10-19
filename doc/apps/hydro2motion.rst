==========================
Kotori hydro2motion README
==========================

Run Kotori DAQ
==============
::

    kotori --config=etc/hydro2motion.ini


Send telemetry data
-------------------
- Open Browser at http://localhost:35000/
- Run::

    h2m-udp-sender "24000;15718;75813;1756;15253;229;220;204;811;1769;0;0;0;0;0;1;0;12;0;0;0;-18;0;4011;417633984;85402624;472851424;0;12242;43;42;0;0"



URL entrypoints
===============

- | InfluxDB UI
  | http://lablab.cicer.de:8083/
- | InfluxDB API
  | http://lablab.cicer.de:8086/
- | Grafana
  | http://lablab.cicer.de:3000/
- | Kotori Telemetry user interface for Hydro2Motion
  | http://lablab.cicer.de:35000/
  | http://h2mdata.cicer.de/
