.. include:: ../../_resources.rst

.. _application-mqttkit:

#######################
The MQTTKit application
#######################


*****
About
*****

| Kotori MQTTKit bundles services for operating an instant-on, generic
| telemetry data sink for collecting sensor data in different scenarios.
|
| The design of MQTTKit specifically addresses data collection in multi-node,
| multi-sensor, environments ¹.
|
| It emphasizes MQTT as communication protocol and JSON as data serialization
| format but implements different other protocols and formats.


**********
Addressing
**********
To successfully publish data to the platform, you should get familiar with the MQTTKit addressing scheme.
We call it the »quadruple hierarchy strategy« and it is reflected on the mqtt bus topic topology.

The topology hierarchy is made up of four identifiers::

    realm / network / gateway / node

The ``realm`` will be configured within the server configuration file
while all other parameters designate the data acquisition channel and
can be used freely by the user.

The topology identifiers are specified as:

- "realm" is the designated root realm. You should prefix the topic name
  with this label when opting in for all features of the telemetry platform.

- "network" is your personal realm, it designates the **owner**.
  Choose anything you like or use an
  `Online UUID Generator <https://www.uuidgenerator.net/>`_
  to gain maximum uniqueness.

- "gateway" is your gateway identifier, it designates a sensor node
  **location** or **group**.
  Choose anything you like.

- "node" is your **node identifier**. Choose anything you like. This usually
  gets transmitted from a sensor device.

In the following examples, this topology address will be encoded into the variable ``CHANNEL``.



*************
Configuration
*************
.. highlight:: ini

Take a look at :download:`etc/examples/mqttkit.ini <../../_static/content/etc/examples/mqttkit.ini>`
as a configuration blueprint.

.. literalinclude:: ../../_static/content/etc/examples/mqttkit.ini
    :language: ini
    :linenos:
    :lines: 1-16
    :emphasize-lines: 11-16



************
Sending data
************
.. highlight:: bash

::

    mosquitto_pub -t mqttkit-1/testdrive/foobar/42/data.json -m '{"temperature": 42.84, "humidity": 83.1}'


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
- See :ref:`basic-mqtt-example` for submitting measurement values /
  telemetry data from the command line.


Advanced
========
- For sending a simple oscillating signal to Kotori from the command line,
  please have a look at the :ref:`sawtooth-signal` page.

- Please follow up at :ref:`daq-mqtt` for transmitting telemetry data
  over MQTT from other environments (Python, Arduino, mbed).

- Also have a look at :ref:`forward-http-to-mqtt` about how to configure
  a HTTP endpoint for your :ref:`application-mqttkit` application and see
  :ref:`daq-http` for transmitting telemetry data over HTTP.


----

| ¹ The design of MQTTKit is derived from vendor :ref:`vendor-hiveeyes`.
