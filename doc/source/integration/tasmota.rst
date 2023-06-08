.. include:: ../_resources.rst

.. _integration-tasmota:
.. _tasmota-decoder:
.. _decoder-tasmota:

#######
Tasmota
#######



*****
About
*****

Receive and record telemetry data from devices running the Tasmota_ firmware using MQTT_.

About Tasmota
=============

Tasmota_ is an alternative firmware for ESP-based devices like the iTead Sonoff. It
features a web UI, rules and timers, OTA updates, custom device templates and sensor
support. It can be controlled over MQTT, HTTP, Serial and KNX for integrations with
smart home systems.

.. figure:: https://tasmota.github.io/docs/_media/frontlogo.svg
    :target: https://tasmota.github.io/docs/_media/frontlogo.svg
    :alt: The Tasmota logo
    :width: 300px

    Tasmota - Open source firmware for ESP devices.

    *Total local control with quick setup and updates. Control using MQTT,
    Web UI, HTTP or serial. Automate using timers, rules or scripts. Integration with
    home automation solutions. Incredibly expandable and flexible.*

.. seealso::

    The `Tasmota documentation`_.


***************
Example devices
***************

.. container:: legroom-md

    .. container:: pull-left

        .. figure:: https://ptrace.getkotori.org/2019-06-04_Sonoff-TH10-TH16.jpg
            :target: https://wiki.iteadstudio.com/Sonoff_TH
            :alt: Sonoff TH: Temperature and Humidity Monitoring WiFi Smart Switch
            :width: 350px

            Sonoff TH: Temperature and Humidity Monitoring WiFi Smart Switch

    .. container:: pull-right

        .. figure:: https://ptrace.getkotori.org/2019-06-04_Sonoff-SC.jpg
            :target: https://wiki.iteadstudio.com/Sonoff_SC
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
    :target: https://tasmota.github.io/docs/MQTT/#configure-mqtt
    :alt: Configure MQTT using WebUI on Tasmota
    :width: 200px

    Configure MQTT using WebUI on Tasmota


Configuration
=============
This is about getting the system configured properly,
so please read this section carefully.

Settings
--------
While configuring the MQTT broker address is straight-forward, special
care should be taken to configure the MQTT topic appropriately to send
telemetry data to the data historian.

| **Topic**: Unique identifier of your device (e.g. hallswitch, kitchen-light). Referenced elsewhere as `%topic%`.
| **Full Topic**: A full topic definition where `%topic%` and `%prefix%` can be interpolated into.

By example
----------
Let's define a communication channel address and a device identifier for
data acquisition.

| **Channel**: ``universe/milky-way/earth-one``
| **Device**: ``node-42``

The appropriate settings for Tasmota would then be

| **Topic**: ``node-42``
| **Full Topic**: ``universe/milky-way/earth-one/%topic%/%prefix%/``

Running this configuration will yield MQTT topics like::

    universe/milky-way/earth-one/node-42/tele/SENSOR
    universe/milky-way/earth-one/node-42/tele/STATE


****************
Payload examples
****************

Submit
======
Acquire an example HTTP payload message of type ``SENSOR`` and publish it to MQTT broker on ``localhost``::

    http https://raw.githubusercontent.com/daq-tools/kotori/main/doc/source/integration/tasmota/sensor-payload.json \
        | mosquitto_pub -h localhost -t universe/milky-way/earth-one/node-42/tele/SENSOR -s

Acquire an example HTTP payload message of type ``STATE`` and publish it to MQTT broker on ``localhost``::

    http https://raw.githubusercontent.com/daq-tools/kotori/main/doc/source/integration/tasmota/state-payload.json \
        | mosquitto_pub -h localhost -t universe/milky-way/earth-one/node-42/tele/STATE -s


Gallery
=======

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
