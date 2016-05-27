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


*************
Configuration
*************
.. highlight:: ini

Take a look at ``etc/examples/mqttkit.ini`` as a configuration blueprint::

    [amazonas]
    type        = application
    realm       = mqttkit-1
    mqtt_topics = mqttkit-1/#
    app_factory = kotori.daq.application.mqttkit:mqttkit_application

.. todo:: Describe how to activate configuration a) in package mode and b) in development mode.


****************
Data acquisition
****************
It is really easy to send data to :ref:`Kotori`
through the MQTT bus from the command line.


Basic
=====
.. highlight:: bash

#. Send measurement values / telemetry data to the "testdrive" channel
   by publishing it to the MQTT_ bus as JSON message::

    # Get hold of a MQTT client of your choice
    aptitude install mosquitto-clients

    # Where to publish measurements
    export MQTT_BROKER=kotori.example.org
    export DEVICE_TOPIC=mqttkit-1/testdrive/area-42/node-1

    # Publish single measurement with multiple values
    mosquitto_pub -h $MQTT_BROKER -t $DEVICE_TOPIC/message-json -m '{"temperature": 42.84, "humidity": 83}'

#. Navigate to the automatically populated Grafana `testdrive dashboard <http://kotori.example.org:3000/dashboard/db/testdrive>`_
   to watch measurement values floating in.


Advanced
========
For sending periodic data to Kotori from the command line,
please have a look at the :ref:`sawtooth-signal` page.


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

