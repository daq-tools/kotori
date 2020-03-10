.. include:: ../../../_resources.rst

.. _daq-mqtt:

####
MQTT
####


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
See :ref:`mqtt-libraries`.


***************
Troubleshooting
***************
.. seealso:: Please read about general :ref:`error-signalling` and :ref:`kotori-troubleshooting`.
