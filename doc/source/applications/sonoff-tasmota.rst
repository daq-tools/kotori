.. include:: ../_resources.rst

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
Receive telemetry data from devices running the `Sonoff-Tasmota`_ firmware.
See also `Add adapter for ingesting data from devices running Sonoff-Tasmota`_.

Here, we are ingesting telemetry data from a Sonoff SC device.
The `Sonoff SC`_ (`wiki <Sonoff SC (Product)_>`_) is an ESP8266 based WiFi
environmental monitoring device. It detects current temperature, humidity,
light intensity, air quality (particulate) and even sound levels (noise pollution).

.. figure:: https://www.itead.cc/wiki/images/thumb/3/36/Sonoff_SC_01.JPG/584px-Sonoff_SC_01.JPG
    :target: https://www.itead.cc/wiki/images/thumb/3/36/Sonoff_SC_01.JPG/584px-Sonoff_SC_01.JPG
    :alt: Sonoff SC environmental monitoring device
    :width: 450px

    Sonoff SC environmental monitoring device


****************
Payload examples
****************

``sonoffSC/tele/STATE``
=======================
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


``sonoffSC/tele/SENSOR``
========================
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
