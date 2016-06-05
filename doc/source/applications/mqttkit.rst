.. include:: ../_resources.rst

.. _application-mqttkit:

#######
MQTTKit
#######

.. contents::
   :local:
   :depth: 1

----

*****
About
*****

    | Kotori MQTTKit bundles services for operating an instant-on, generic
    | telemetry data sink for collecting sensor data in different scenarios.
    |
    | It uses MQTT as communication protocol
    | and JSON as data serialization format.
    |
    | MQTTKit specifically addresses data collection in multi-node, multi-sensor
    | environments as its design is directly derived from vendor :ref:`vendor-hiveeyes`.

.. todo::

    Write some words about the mqtt bus topic topology (``mqttkit-1/testdrive/area-42/node-1``) used here.
    In the meanwhile, please have a look at the :ref:`hiveeyes:hiveeyes-one-topology`.


*************
Configuration
*************
.. highlight:: ini

Take a look at :download:`etc/examples/mqttkit.ini <../_static/content/etc/examples/mqttkit.ini>`
as a configuration blueprint.

.. literalinclude:: ../_static/content/etc/examples/mqttkit.ini
    :language: ini
    :linenos:
    :lines: 1-16
    :emphasize-lines: 11-16

.. todo:: Describe how to activate configuration a) in package mode and b) in development mode.


**************
Receiving data
**************
.. highlight:: bash

::

    # Receive telemetry data by subscribing to MQTT topic
    mosquitto_sub -t mqttkit-1/#


****************
Data acquisition
****************
It is really easy to transmit telemetry data to
:ref:`Kotori` in different ways over the MQTT bus.

Basic
=====
#. Send measurement values / telemetry data to the "testdrive" channel from the command line::

    # Setup "mosquitto_pub"
    aptitude install mosquitto-clients

    # Where to send data to
    export MQTT_BROKER=kotori.example.org
    export MQTT_TOPIC=mqttkit-1/testdrive/area-42/node-1

    # Define an example sensor emitting a single sample of a sawtooth signal in JSON format
    sensor() { echo "{\"sawtooth\": $(date +%-S)}"; }

    # Define the transmission command to send telemetry data to the "testdrive" network
    transmitter() { mosquitto_pub -h $MQTT_BROKER -t $MQTT_TOPIC/message-json -l; }

    # Acquire and transmit a single sensor reading
    sensor | transmitter

#. Navigate to the automatically populated Grafana `testdrive dashboard <http://kotori.example.org:3000/dashboard/db/testdrive>`_
   to watch measurement values floating in.

.. tip::

    Please follow up at :ref:`daq-mqtt` for transmitting telemetry data
    over MQTT from other environments (Python, Arduino, mbed).


Advanced
========
- For sending a simple oscillating signal to Kotori from the command line,
  please have a look at the :ref:`sawtooth-signal` page.

- Also have a look at :ref:`forward-http-to-mqtt` about how to configure
  a HTTP endpoint for your :ref:`application-mqttkit` application and see
  :ref:`daq-http` for transmitting telemetry data over HTTP.


**********
Operations
**********

Kotori
======
It is recommended to start Kotori in debug mode like::

    kotori --debug-mqtt --debug-influx


Database
========
For dropping the InfluxDB database using its HTTP API::

    export INFLUXDB_HOST=kotori.example.org
    curl --silent --get "http://$INFLUXDB_HOST:8086/query?pretty=true" --user admin:admin --data-urlencode 'q=DROP DATABASE "mqttkit_1_testdrive"'

