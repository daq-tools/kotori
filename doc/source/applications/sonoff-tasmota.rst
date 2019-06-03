.. include:: ../_resources.rst

.. _application-tasmota:

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

.. _Sonoff-Tasmota: https://github.com/arendst/Sonoff-Tasmota
.. _Add adapter for ingesting data from devices running Sonoff-Tasmota: https://github.com/daq-tools/kotori/issues/10


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
