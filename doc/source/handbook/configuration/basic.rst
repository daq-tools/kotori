.. include:: ../../_resources.rst

.. _application-basic:

#################
Basic application
#################


*****
About
*****
A basic telemetry data collection application
for collecting sensor data in local setups.

It emphasizes MQTT as communication protocol and JSON as data serialization
format but implements different other protocols and formats.


*************
Configuration
*************
.. highlight:: ini

The core of each data acquisition application is its configuration object.
The file :download:`etc/examples/basic.ini <../../_static/content/etc/examples/basic.ini>`
can be used as a configuration blueprint.

This configuration snippet will create an
application object defined as ``[basic]``.

.. literalinclude:: ../../_static/content/etc/examples/basic.ini
    :language: ini
    :linenos:
    :lines: 1-16
    :emphasize-lines: 10-15


**********
Addressing
**********
To successfully publish data to the platform, let's imagine
a basic addressing scheme like::

    realm / node

The ``realm`` will be configured within the server configuration file
while the ``node`` parameter will designate the data acquisition channel
and can be assigned by the user.

The topology identifiers are specified as:

- "realm" is the designated root realm. You should prefix the topic name
  with this label when opting in for all features of the telemetry platform.

- "node" is your **node identifier**. Choose anything you like. This usually
  gets transmitted from a sensor device.



************
Sending data
************
In the following examples, the topology address
will be encoded into the variable ``CHANNEL``.

.. highlight:: bash

::

    # Define channel and data.
    CHANNEL=basic/node42
    DATA='{"temperature": 42.84, "humidity": 83.1}'

    # Publish telemetry data to MQTT topic.
    echo "$DATA" | mosquitto_pub -t $CHANNEL/data.json -l


**************
Receiving data
**************

.. highlight:: bash

::

    # Receive telemetry data by subscribing to MQTT topic.
    mosquitto_sub -t basic/#
