.. include:: ../../_resources.rst

.. _application-object:

#########################
Application configuration
#########################


************
Introduction
************
The core of each data acquisition application is its configuration object.


*************
Configuration
*************
This configuration snippet will create an
application object defined as ``[amazonas]``.

::

    ; -----------------------------
    ; Data acquisition through MQTT
    ; -----------------------------
    [amazonas]
    enable      = true
    type        = application
    realm       = amazonas
    mqtt_topics = amazonas/#
    application = kotori.daq.application.mqttkit:mqttkit_application


***********
Description
***********
This essentially spawns an application on the realm ``amazonas``.

- The realm -- here called ``amazonas`` -- designates the "tenant"
  or "vendor" by means of a multi-tenant system.
- Kotori will subscribe to the MQTT topic ``amazonas/#``
  to receive all readings published to that topic.
- When data is received, the data payload will be evaluated
  through the machinery defined through the software component
  ``kotori.daq.application.mqttkit``.
  This component is assembled from several baseline
  software components from the toolbox of Kotori.
- Kotori will also signal Grafana_ in order to create some instant dashboards
  reflecting the telemetry fields of the measurement data just ingested.


*******
Details
*******

WAN addressing
==============
One of the convention of the `MQTTKit communication flavor`_
is that is uses several MQTT topic segments implementing the
»quadruple hierarchy strategy« in a wide-network addressing
scheme like outlined within the `MQTTKit addressing scheme`_::

    realm / network / gateway / node

Implementation details
======================
The main workhorse here is definitively MqttInfluxGrafanaService_,
which is spun up through `mqttkit.py <https://github.com/daq-tools/kotori/blob/0.24.5/kotori/daq/application/mqttkit.py#L26-L32>`_,
essentially tying all things together.

The addressing scheme is implemented through the WanBusStrategy_ component
used within MqttInfluxGrafanaService_. It will take the responsibility of
properly receiving and decoding message payloads arriving on the MQTT bus
according to the specific conventions implemented in there.
