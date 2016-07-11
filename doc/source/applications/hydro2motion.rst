.. include:: ../_resources.rst

.. _vendor-hydro2motion:

============
Hydro2Motion
============

.. contents::
   :local:
   :depth: 1

----

.. highlight:: bash

*****
About
*****

Introduction
============
Kotori powered the telemetry platform for the Hydro2Motion_ team
at the "`Shell Eco-marathon europe`_ 2015" in Rotterdam.
This is a fine project from `Labor für Systemtechnik`_ fame
at the `Munich University of Applied Sciences`_.

They have an article about the event at their blog: `Hydro2Motion at Shell Eco-Marathon 2015 in Rotterdam`_.
We also have some impressions:

.. figure:: https://ptrace.isarengineering.de/2016-06-05_H2M-2015-DSC07107-300x200.jpg
    :target: https://ptrace.isarengineering.de/2016-06-05_H2M-2015-DSC07107.jpg
    :alt: On the way
    :width: 450px
    :align: left

    On the way

.. figure:: https://ptrace.isarengineering.de/2016-06-05_H2M-2015-DSC07514-300x200.jpg
    :target: https://ptrace.isarengineering.de/2016-06-05_H2M-2015-DSC07514.jpg
    :alt: Getting ready
    :width: 450px
    :align: right

    Getting ready

|clearfix|

.. figure:: https://ptrace.isarengineering.de/2016-03-07_h2m-racing-rotterdam2015.jpg
    :alt: Racing
    :width: 450px
    :align: left

    Racing

|clearfix|


The vehicle
===========

.. figure:: https://ptrace.isarengineering.de/2016-03-07_h2m-mission-72.jpg
    :target: https://ptrace.isarengineering.de/2016-03-07_h2m-mission-150.jpg
    :alt: Mission
    :width: 450px


The fuel cell
=============
Their vehicle is powered by a hydrogen fuel cell.

.. figure:: https://ptrace.isarengineering.de/2016-03-07_h2m-fuel-cell-component.jpg
    :alt: Fuel cell component
    :width: 450px
    :align: left

    Fuel cell component

.. figure:: https://ptrace.isarengineering.de/2016-03-07_h2m-fuel-cell-vehicle.jpg
    :alt: Fuel cell in vehicle
    :width: 450px
    :align: right

    Fuel cell in vehicle

|clearfix|

Its auxiliary equipment emits telemetry data.

.. figure:: https://ptrace.isarengineering.de/2016-03-07_h2m-fuel-cell-schematics-72.jpg
    :target: https://ptrace.isarengineering.de/2016-03-07_h2m-fuel-cell-schematics-150.jpg
    :alt: Fuel cell schematics
    :width: 450px
    :align: left

    Fuel cell schematics

.. container:: align-right

    .. csv-table:: Ethernet Packet out (Typ 1), 2013-10-25
        :header: Offset, Size, Variable, Transfer, Unit
        :widths: 5, 5, 10, 10, 10
        :delim: ;

        1;	2;	MSG ID;	1-9;
        3;	6;	V FC;	0 - 40000;	mV
        9;	6;	V CAP;	0 - 40000;	mV
        15;	6;	A to Eng;	0 - 16000;	mA
        21;	6;	A to CAP;	0 - 16000;	mA
        27;	4;	T Air in ;	0 - 500;	°C*10
        31;	4;	T Air out;	0 - 900;	°C*10
        35;	4;	T FC H2O out;	0 - 800;	°C*10
        39;	5;	Water in;	0 - 999;	mg/l (luft)
        44;	5;	Water out;	0 - 999;	mg/l (luft)
        49;	2;	Master SW;	0/1;	Hauptschalter
        51;	2;	CAP Down SW;	0/1;	Ladeabsenkung
        53;	2;	Drive SW;	0/1;	Fahrschalter
        55;	2;	FC state;	0/1;	Zellenzustand
        57;	2;	Mosfet state;	0/1;	Mosfetzustand
        59;	2;	Safty state;	0/1;	Sicherheitskreis
        61;	4;	Air Pump load;	0 - 100;	%
        65;	4;	Mosfet load;	0 - 100;	%
        69;	4;	Water Pump ;	0 - 100;	%
        73;	4;	Fan load;	0 - 100;	%
        77;	5;	Acc X;	+- 999;	mg
        82;	5;	Acc Y;	+- 999;	mg
        87;	5;	Acc Z;	+- 999;	mg
        92;	5;	Stearing angle;	+- 200;	°*10
        97;	9;	GPS x;	+- 6999999;	m
        106;	9;	GPS y;	+- 6999999;	m
        115;	9;	GPS z;	+- 6999999;	m
        124;	4;	GPS Speed;	0-200;	m/s * 10
        128;	4;	V Safty;	0-200;	V*10
        132;	4;	H2 Level;	0-150;	%
        136;	5;	Eng. RPM;	0-9999;	1/min


|clearfix|


.. note::

    Hydro2Motion presented a part of its design process -
    the `Case study of simulation-driven designed components for a hydrogen-powered prototype vehicle`_ -
    at the ATC 2015 conference in Paris.


***********
Environment
***********
Let's have a look at the environment:

- Mbed_ is a popular embedded computing platform used intensively here.
- Telemetry data is transmitted from sensor nodes over a GPRS_/UMTS_/LTE_ cell network uplink.
  The network transport is UDP/IP, the data serialization format is plain CSV::

    24000;15718;75813;1756;15253;229;220;204;811;1769;0;0;0;0;0;1;0;12;0;0;0;-18;0;4011;417633984;85402624;472851424;0;12242;43;42;0;0


***************
System overview
***************

.. graphviz:: hydro2motion.dot

- Receive telemetry messages over UDP in CSV format.
- Manually decode messages in a Python callback handler.
- Convert, munge and enrich data by using imperative code, no DSL in sight.
- Store measurements to the InfluxDB_ timeseries database.
- Automatically create Grafana_ panels for instant telemetry data visualization.

    .. figure:: https://ptrace.isarengineering.de/2016-03-07_h2m-telemetry-72.jpg
        :target: https://ptrace.isarengineering.de/2016-03-07_h2m-telemetry-150.jpg
        :alt: Live telemetry with Grafana
        :width: 450px
        :align: left

        Live telemetry with Grafana

|clearfix|

- Publish telemetry data to the WAMP_ bus.
- Subscribe to WAMP_ data streams inside the web browser and process the data points.

    .. figure:: https://ptrace.isarengineering.de/2016-06-05_H2M-2015-Kotori-Dashboard.png
        :target: `Live Telemetry at Hydro2Motion`_
        :alt: Live telemetry with GPS position on map
        :width: 450px

        Live telemetry with GPS position on map (`article in german <Live Telemetrie at Hydro2Motion_>`_)

        - GPS map: Draw a pin on a map widget at the GPS position of the vehicle using Leaflet_.
        - Oscilloscope: Display received data points in an "osci-style" widget, based on Rickshaw_.

|clearfix|

.. note::

    While this communication layer was based on CSV-over-UDP,
    the next iteration is based on Binary-over-UDP.
    This transport communicates more efficiently while still retaining a maximum of convenience:
    We managed to send opaque binary blobs over air and wire but can decode
    the payloads from knowledge of information of a standard C/C++ header file.
    See also the :ref:`data acquisition system for vendor "LST" <vendor-lst>` for more
    information about this.


*******************
Platform operations
*******************
This section is about running the whole platform on your own hardware.
Please be aware this is a work in progress. We are happy to receive
valuable feedback for improving things gradually.

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


**************
Platform usage
**************
The platform is hosted at the `Kotori Telemetry Dashboard for Hydro2Motion`_.


URL entrypoints
===============

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

    export INFLUX_URI=http://localhost:8086/query?pretty=true
    curl --silent --get $INFLUX_URI --user admin:admin --data-urlencode 'db=hydro2motion' --data-urlencode 'q=select * from "telemetry";' | jq '.'

