.. include:: ../../_resources.rst

.. _data-acquisition:

.. _kotori-client-handbook:

################
Data acquisition
################


************
Introduction
************
:ref:`Kotori` offers communication paths for data
acquisition from different kinds of sensor nodes.
Check our list of favourite client libraries.


*********
Protocols
*********

.. toctree::
    :maxdepth: 1
    :glob:

    protocol/mqtt
    protocol/http
    protocol/udp


*****************
Language runtimes
*****************

.. toctree::
    :maxdepth: 1
    :glob:

    runtime/bash
    runtime/arduino
    runtime/python
    runtime/micropython
    runtime/lua-nodemcu
    runtime/javascript
    runtime/php


*******************
Firmware frameworks
*******************

.. toctree::
    :maxdepth: 1
    :glob:

    runtime/homie
    ../decoders/tasmota


*********************
Serialization formats
*********************

.. toctree::
    :maxdepth: 1
    :glob:

    format/struct
    format/bencode


*******************
Metadata signalling
*******************

.. toctree::
    :maxdepth: 1
    :glob:

    timestamp
    error-signalling


********
Examples
********

A :ref:`sawtooth-signal` is convenient to publish
measurement values without having any hardware in place.
