.. include:: ../../_resources.rst

.. _forward-http-to-mqtt:

#######################
Forwarding HTTP to MQTT
#######################

************
Introduction
************
For enabling data acquisition via HTTP, just forward
payloads of POST or PUT requests to the MQTT bus and
let the downstream infrastructure :ref:`application-mqttkit`
handle all the rest.

*****
Setup
*****
This can be achieved by configuring a generic HTTP-to-MQTT
forwarder application:

.. literalinclude:: ../../_static/content/etc/examples/forwarders/http-to-mqtt.ini
    :language: ini
    :linenos:
    :emphasize-lines: 34-42


.. tip::

    Also have a look at :ref:`daq-http` for different ways to transmit telemetry data over HTTP.

