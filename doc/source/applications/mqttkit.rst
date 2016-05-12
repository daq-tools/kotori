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
MQTTKit bundles services for operating an instant-on, generic telemetry
data sink for collecting sensor data in different scenarios.

MQTTKit uses MQTT as communication protocol and JSON as data serialization format.


*************
Configuration
*************
Take a look at ``etc/examples/mqttkit.ini`` as a configuration blueprint. You might use a snippet like::

    [amazonas]
    type        = application
    realm       = amazonas
    mqtt_topics = amazonas/#
    app_factory = kotori.daq.application.mqttkit:mqttkit_application


********
Synopsis
********
For submitting telemetry data, just publish JSON messages to the MQTT broker::

    mosquitto_pub -t amazonas/ecuador/cuyabeno/1/message-json -m '{"temperature": 42.84, "humidity": 83}'

