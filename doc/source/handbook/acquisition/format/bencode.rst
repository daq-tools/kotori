.. include:: ../../../_resources.rst

###############################
Data serialization with Bencode
###############################


********
Examples
********

Hiveeyes
========
The :ref:`vendor-hiveeyes` project for collaborative beehive
monitoring has a family of sensor nodes transmitting telemetry
data over radio:

- :ref:`hiveeyes-one` sensor nodes transmit data to a gateway using RF,
  the gateway receives and decodes telemetry data from Bencode_ format,
  then forwards it to the MQTT_ broker in JSON.
  This is specified in :ref:`beradio-spec` and implemented
  in Python using the serial-to-mqtt forwarder :ref:`beradio-python <beradio-python>`.

