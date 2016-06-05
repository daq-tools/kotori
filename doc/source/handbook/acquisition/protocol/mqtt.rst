.. include:: ../../../_resources.rst

.. _daq-mqtt:

##########################
Data acquisition over MQTT
##########################

************
MQTT clients
************

.. list-table:: List of Kotori MQTT clients
   :widths: 5 40
   :header-rows: 1
   :class: table-generous

   * - Name
     - Description

   * - mosquitto_pub
     - For getting started with a basic example, read how to
       :ref:`generate a dynamic, slowly oscillating sawtooth signal and publish it to MQTT <sawtooth-mqtt>`.

   * - Python
     - Libraries

       - `paho-mqtt`_, the MQTT Python client library of the `Eclipse Paho`_ project

       Examples

       .. admonition:: Todo
           :class: admonition-todo admonition-smaller

           Add complete example program. In the meanwhile, have a look at
           the serial-to-mqtt forwarder :ref:`beradio-python <beradio-python>`
           of the :ref:`Hiveeyes project <hiveeyes>`.

   * - Arduino
     - Libraries

       - `Arduino Client for MQTT`_ by `Nick O'Leary`_
       - `async-mqtt-client`_ by `Marvin Roger`_ (for ESP8266)
       - `Adafruit MQTT Library`_ from Adafruit_

       Examples

       .. admonition:: Todo
           :class: admonition-todo admonition-smaller

           Add complete example program. In the meanwhile, have a look at
           the :ref:`Hiveeyes <hiveeyes>` ESP8266-based sensor node code `node-wifi-mqtt.ino`_.

   * - ARMmbed
     - `ARMmbed ESP8266 MQTT example`_

.. _node-wifi-mqtt.ino: https://github.com/hiveeyes/arduino/blob/master/node-wifi-mqtt/src/node-wifi-mqtt.ino


.. _daq-mqtt-bash:

Command line
============
.. todo::

    - Add example from Hiveeyes, link here.
    - Also add link from handbook/kotori and setup/getting-started to here.


----


********
Examples
********

.. todo:: Refactor to acquisition/examples

Hiveeyes
========
The :ref:`vendor-hiveeyes` project for collaborative beehive
monitoring uses two different kinds of sensor nodes.

- :ref:`hiveeyes-one` sensor nodes transmit data to a gateway using RF,
  the gateway receives and decodes telemetry data from Bencode_ format,
  then forwards it to the MQTT_ broker in JSON.
  This is specified in :ref:`beradio-spec` and implemented
  in Python using the serial-to-mqtt forwarder :ref:`beradio-python <beradio-python>`.

- :ref:`open-hive` sensor nodes based on the *Adafruit HUZZAH ESP8266*
  directly send telemetry data to the MQTT_ broker in JSON format.

