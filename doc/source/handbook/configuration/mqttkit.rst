.. include:: ../../_resources.rst

.. _application-mqttkit:

###################
MQTTKit application
###################


*****
About
*****
A generic distributed monitoring platform for
collecting sensor data in wide area network setups
and multi-node, multi-sensor environments ¹.

It emphasizes MQTT as communication protocol and JSON as data serialization
format but implements different other protocols and formats.


*************
Configuration
*************
.. highlight:: ini

The core of each data acquisition application is its configuration object.
The file :download:`etc/examples/mqttkit.ini <../../_static/content/etc/examples/mqttkit.ini>`
can be used as a configuration blueprint.

This configuration snippet will create an
application object defined as ``[mqttkit-1]``.

.. literalinclude:: ../../_static/content/etc/examples/mqttkit.ini
    :language: ini
    :linenos:
    :lines: 1-16
    :emphasize-lines: 10-15


**********
Addressing
**********
To successfully publish data to the platform, you should get familiar with the MQTTKit addressing scheme.
We call it the »quadruple hierarchy strategy« and it is reflected on the mqtt bus topic topology.

The topology hierarchy is made up of four identifiers::

    realm / network / gateway / node

The ``realm`` will be configured within the server configuration file
while all other parameters designate the data acquisition channel and
can be assigned by the user.

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



************
Sending data
************
In the following examples, the topology address
will be encoded into the variable ``CHANNEL``.

.. highlight:: bash

::

    # Define channel and data.
    CHANNEL=mqttkit-1/testdrive/foobar/42
    DATA='{"temperature": 42.84, "humidity": 83.1}'

    # Publish telemetry data to MQTT topic.
    echo "$DATA" | mosquitto_pub -t $CHANNEL/data.json -l


**************
Receiving data
**************
.. highlight:: bash

::

    # Receive telemetry data by subscribing to MQTT topic
    mosquitto_sub -t mqttkit-1/#


----

| ¹ The design of MQTTKit is derived from vendor :ref:`vendor-hiveeyes`.
