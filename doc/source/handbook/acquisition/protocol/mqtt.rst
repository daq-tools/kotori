.. include:: ../../../_resources.rst

.. _daq-mqtt:

##########################
Data acquisition over MQTT
##########################

.. contents::
   :local:
   :depth: 1


************
Introduction
************
Measurement readings can be acquired through MQTT using JSON.


*****
Setup
*****
Please have a look at :ref:`application-mqttkit` about how to configure a MQTT application.


**************
Basic examples
**************
.. highlight:: bash

Setup "mosquitto_pub"::

    aptitude install mosquitto-clients

Define where to send data to::

    export MQTT_BROKER=localhost
    export MQTT_TOPIC=mqttkit-1/testdrive/area-42/node-1


Single readings
===============
Publish single sensor readings::

    mosquitto_pub -h $MQTT_BROKER -t $MQTT_TOPIC/data/temperature -m '42.84'


Multiple readings
=================
Publish multiple sensor readings using JSON::

    mosquitto_pub -h $MQTT_BROKER -t $MQTT_TOPIC/data.json -m '{"temperature": 42.84, "humidity": 83}'


.. _daq-mqtt-with-timestamp:

Readings with timestamp
=======================
Publish sensor reading with timestamp in `ISO 8601`_ format::

    mosquitto_pub -h $MQTT_BROKER -t $MQTT_TOPIC/data.json -m '{"time": "2016-12-07T17:30:15Z", "temperature": 42.84, "humidity": 83}'

See also the whole list of :ref:`daq-timestamp-formats`.


.. _daq-mqtt-annotation:

Annotations
===========
`Grafana Annotations`_ can be created through MQTT at the ``/event.json`` topic suffix.
While arbitrary fields can be submitted, Grafana_ evaluates the fields ``title``, ``text`` and ``tags``.
It is possible to use HTML inside the ``text`` field, for example to link this event to another web application.

The synopsis is::

    mosquitto_pub -h $MQTT_BROKER -t $MQTT_TOPIC/event.json -m '{"title": "Some event", "text": "<a href=\"https://somewhere.example.org/events?reference=482a38ce-791e-11e6-b152-7cd1c55000be\">see also</a>", "tags": "event,alert,important", "reference": "482a38ce-791e-11e6-b152-7cd1c55000be"}'

Annotations can also be submitted retroactively, just add a ``time`` field::

    mosquitto_pub -h $MQTT_BROKER -t $MQTT_TOPIC/event.json -m '{"time": "2016-12-07T17:30:15.842428Z", "title": "Some event in the past"}'

See also the whole list of :ref:`daq-timestamp-formats`.


.. _daq-mqtt-csv:

**********
CSV format
**********
.. todo:: Not implemented yet.


****************************
Periodic acquisition example
****************************

Sawtooth
========
The characteristics of sawtooth signals (dynamic, slowly oscillating)
are convenient to generate measurement sensor readings and publish
telemetry data without having any hardware in place.

For getting started, please read about how to
:ref:`generate a dynamic, slowly oscillating sawtooth signal and publish it to MQTT <sawtooth-mqtt>`.


*****************
Language bindings
*****************

.. list-table:: List of Kotori MQTT clients
   :widths: 5 40
   :header-rows: 1
   :class: table-generous

   * - Name
     - Description

   * - Python
     - - Libraries

            - `paho-mqtt`_, the MQTT Python client library of the `Eclipse Paho`_ project.

       - Examples

            - See a :ref:`basic MQTT example in Python <daq-python-mqtt>`.

   * - Arduino
     - - Libraries

            - `Arduino Client for MQTT`_ by `Nick O'Leary`_
            - `Adafruit MQTT Library`_ from Adafruit_

       - Examples

            - The :ref:`Hiveeyes <hiveeyes>` ESP8266-based sensor node firmwares `node-wifi-mqtt.ino`_
              and `node-wifi-mqtt-homie.ino`_.

   * - Arduino/ESP8266
     - - Libraries

            - `esp_mqtt`_, the `Native MQTT client library for ESP8266`_ by Tuan PM
            - `async-mqtt-client`_ by `Marvin Roger`_

   * - ARMmbed
     - - Libraries

            - The `ARMmbed MQTT library`_, a port of the `Eclipse Paho Embedded MQTT C/C++ Client Libraries`_.

       - Examples

            - `ARMmbed ESP8266 MQTT example`_


***************
Troubleshooting
***************
.. todo:: Add notes about no data appearing in Grafana, etc.


----


************
Applications
************

.. todo:: Refactor to acquisition/examples

.. _daq-mqtt-bash:

Command line
============
.. todo::

    - Add example from Hiveeyes, link here.
    - Also add link from handbook/kotori and setup/getting-started to here.

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

