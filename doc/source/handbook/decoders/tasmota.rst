.. include:: ../../_resources.rst

.. _decoder-tasmota:

#######
Tasmota
#######

.. contents::
   :local:
   :depth: 1

----


*****
About
*****
Ingest telemetry data from devices running the Tasmota_ firmware using MQTT_.


*******
Devices
*******

.. container:: legroom-md

    .. container:: pull-left

        .. figure:: https://ptrace.getkotori.org/2019-06-04_Sonoff-TH10-TH16.jpg
            :target: https://www.itead.cc/smart-home/sonoff-th.html
            :alt: Sonoff TH: Temperature and Humidity Monitoring WiFi Smart Switch
            :width: 350px

            Sonoff TH: Temperature and Humidity Monitoring WiFi Smart Switch

    .. container:: pull-right

        .. figure:: https://ptrace.getkotori.org/2019-06-04_Sonoff-SC.jpg
            :target: https://www.itead.cc/wiki/Sonoff_SC
            :alt: Sonoff SC: Environmental monitoring device
            :width: 350px

            Sonoff SC: Environmental monitoring device

|clearfix|


Sonoff TH
=========
The `Sonoff TH`_ (`product page <Sonoff TH (Product)_>`_) is an environmental
monitoring and controlling device for measuring current temperature and humidity.


Sonoff SC
=========
The `Sonoff SC`_ (`product page <Sonoff SC (Product)_>`_) is an environmental
monitoring device for measuring current temperature, humidity, light intensity,
air quality (particulates) and sound levels (noise pollution).



*****************
Grafana Dashboard
*****************

.. figure:: https://ptrace.getkotori.org/2019-06-04_Sonoff-SC-Tasmota-RFA.png
    :alt: Grafana Dashboard for Sonoff SC environmental monitoring device
    :target: https://ptrace.getkotori.org/2019-06-04_Sonoff-SC-Tasmota-RFA.png

    Grafana Dashboard for Sonoff SC environmental monitoring device



********
Firmware
********
Tasmota_ is an alternative firmware for ESP8266-based devices
like the iTead Sonoff. It features a web UI, rules and timers, OTA updates,
custom device templates and sensor support. It can be controlled over
MQTT, HTTP, Serial and KNX for integrations with smart home systems.


************
Device setup
************
By staying as close to the vanilla documentation examples as possible,
newcomers should have an easy way getting their telemetry data ingested.
Kotori will recognize the Tasmota device by its MQTT topic suffix like
``SENSOR`` or ``STATE`` and will route telemetry messages through the
appropriate decoding machinery.


Introduction
============
See also `Configure MQTT for the Tasmota Firmware`_.

.. figure:: https://user-images.githubusercontent.com/5904370/53048775-d3d16e00-3495-11e9-8917-70b56451ebeb.png
    :target: https://github.com/arendst/Tasmota/wiki/MQTT#configure-mqtt
    :alt: Configure MQTT using WebUI on Tasmota
    :width: 200px

    Configure MQTT using WebUI on Tasmota


Configuration
=============
This section is about getting the system configured
properly, so please read this section carefully.

Settings
--------
While configuring the MQTT broker address is straight-forward, special
care should be taken to configure the MQTT topic appropriately to send
telemetry data to the data historian.

:Topic: Unique identifier of your device (e.g. hallswitch, kitchen-light). Referenced elsewhere as `%topic%`.
:Full Topic: A full topic definition where `%topic%` and `%prefix%` can be interpolated into.

By example
----------
Let's define a communication channel address and a device identifier for
data acquisition.

:Channel: ``universe/milky-way/earth-one``
:Device: ``node-42``

The appropriate settings for Tasmota would then be

:Topic: ``node-42``
:Full Topic: ``universe/milky-way/earth-one/%topic%/%prefix%/``

Reflections
-----------
So, the data logger device is called ``node-42`` and it will send telemetry
data to the communication channel ``universe/milky-way/earth-one``.
By decomposing the channel address, we can understand the purpose of each
addressing component.

:realm: ``universe``
:owner: ``milky-way``
:site: ``earth-one``
:node: ``node-42``

Running this configuration will yield MQTT topics like::

    universe/milky-way/earth-one/node-42/tele/SENSOR
    universe/milky-way/earth-one/node-42/tele/STATE


***********
Development
***********

Work in progress
================
The development of this decoder has been sparked at `Add adapter for ingesting data from devices running Tasmota`_.
We are happy to receive contributions of any kind.

- https://github.com/arendst/Tasmota/issues/975
- https://github.com/arendst/Tasmota/issues/1430


Submit example payload
======================
Acquire an example HTTP payload message of type ``SENSOR`` and publish it to MQTT broker on ``localhost``::

    http https://raw.githubusercontent.com/daq-tools/kotori/master/doc/source/handbook/decoders/tasmota/sensor-payload.json \
        | mosquitto_pub -h localhost -t universe/milky-way/earth-one/node-42/tele/SENSOR -s

Acquire an example HTTP payload message of type ``STATE`` and publish it to MQTT broker on ``localhost``::

    http https://raw.githubusercontent.com/daq-tools/kotori/master/doc/source/handbook/decoders/tasmota/state-payload.json \
        | mosquitto_pub -h localhost -t universe/milky-way/earth-one/node-42/tele/STATE -s


********
Appendix
********

Payload examples
================

``sonoffSC/tele/SENSOR``
------------------------
::

    {
      "Time": "2019-06-02T22:13:07",
      "SonoffSC": {
        "Temperature": 25,
        "Humidity": 15,
        "Light": 20,
        "Noise": 10,
        "AirQuality": 90
      },
      "TempUnit": "C"
    }

::

    {
      "Time": "2017-02-16T10:13:52",
      "DS18B20": {
        "Temperature": 20.6
      }
    }

``sonoffSC/tele/STATE``
-----------------------
::

    {
      "Time": "2019-06-02T22:13:07",
      "Uptime": "1T18:10:35",
      "Vcc": 3.182,
      "SleepMode": "Dynamic",
      "Sleep": 50,
      "LoadAvg": 19,
      "Wifi": {
        "AP": 1,
        "SSId": "{redacted}",
        "BSSId": "A0:F3:C1:{redacted}",
        "Channel": 1,
        "RSSI": 100,
        "LinkCount": 1,
        "Downtime": "0T00:00:07"
      }
    }
