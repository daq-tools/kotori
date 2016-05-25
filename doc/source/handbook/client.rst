.. include:: ../_resources.rst

.. _kotori-client-handbook:

###############
Client Handbook
###############


************
Introduction
************
Hiveeyes offers communication paths for data
acquisition from different kinds of sensor nodes.
Check our list of favourite client libraries.


****
JSON
****

Python
======
.. highlight:: python

Batteries included::

    >>> import json
    >>> json.dumps({"hello": "world"})
    '{"hello": "world"}'

Arduino
=======
.. highlight:: cpp

`Arduino JSON library`_, an elegant and efficient JSON library for embedded systems::

    StaticJsonBuffer<200> jsonBuffer;

    JsonObject& root = jsonBuffer.createObject();

    // sensor name
    root["sensor"] = "gps";
    root["time"]   = 1351824120;

    JsonArray& data = root.createNestedArray("data");
    data.add(48.756080, 6);  // 6 is the number of decimals to use. default: 2
    data.add(2.302038, 6);

    root.printTo(Serial);
    // This prints:
    // {"sensor":"gps","time":1351824120,"data":[48.756080,2.302038]}



****
MQTT
****
- Python

    - `paho-mqtt`_, `Eclipse Paho`_ MQTT Python client library

- Arduino

    - `Arduino Client for MQTT`_ (recommended)
    - `Adafruit MQTT Library`_ (confirmed to work)

- ESP8266/mbed

    - `ARMmbed ESP8266 MQTT example`_


******
Binary
******
.. todo:: Better describe :ref:`vendor-lst`.


***
UDP
***
.. todo:: Better describe :ref:`vendor-hydro2motion`.


********
Examples
********

Hiveeyes
========
The :ref:`vendor-hiveeyes` project for collaborative beehive
monitoring uses two different kinds of sensor nodes.

- :ref:`hiveeyes-one` sensor nodes transmit data to a gateway using RF,
  the gateway receives and decodes telemetry data from Bencode_ format,
  then forwards it to the MQTT_ broker in JSON.
  This is specified in :ref:`beradio-spec` and implemented
  in Python using the serial-to-mqtt forwarder :ref:`beradio-python <beradio-python>`.

- :ref:`open-hive` sensor nodes based on the *Adafruit HUZZAH ESP8266*
  directly send telemetry data to the MQTT_ broker in JSON format.

