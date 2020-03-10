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


*************
DAQ protocols
*************

.. toctree::
    :maxdepth: 1

    protocol/mqtt
    protocol/http
    protocol/udp


**********************
Events and Annotations
**********************

.. toctree::
    :maxdepth: 1

    events


*******************
Metadata signalling
*******************

.. toctree::
    :maxdepth: 1

    timestamp
    error-signalling


*********************
Serialization formats
*********************

.. toctree::
    :maxdepth: 1

    format/struct
    format/bencode


********
Examples
********

A :ref:`sawtooth-signal` is convenient to publish
measurement values without having any hardware in place.
