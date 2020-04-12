.. include:: ../../_resources.rst

.. _http-api:
.. _forward-http-to-mqtt:

##################################
HTTP acquisition API configuration
##################################

************
Introduction
************
Data acquisition via HTTP works by forwarding HTTP payloads from
POST or PUT requests to the MQTT bus.
The downstream infrastructure :ref:`application-mqttkit`
will handle all the rest.

*****
Setup
*****
This can be achieved by configuring a generic HTTP-to-MQTT
forwarder application:

.. literalinclude:: ../../_static/content/etc/examples/forwarders/http-api-generic.ini
    :language: ini
    :linenos:
    :emphasize-lines: 34-42


.. tip::

    Also have a look at :ref:`daq-http` for different ways to transmit telemetry data over HTTP.

