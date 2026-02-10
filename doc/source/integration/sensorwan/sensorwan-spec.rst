.. include:: ../../_resources.rst

.. _sensorwan-spec:

###########################
SensorWAN 3.0 specification
###########################

.. highlight:: text

*****
About
*****

The SensorWAN channel addressing scheme can be used for assigning telemetry
data communication channels to individual `sensor nodes`_ in wide-area `sensor
network`_ scenarios, or similar multi-node, multi-sensor environments.


***********
Description
***********

The addressing scheme is essentially a path string using exactly four address
components.

::

    <realm>/<network>/<group>/<name>

As such, it maps 1:1 to MQTT topics and HTTP URL paths, and provides other means
for protocols which do not support path-based addressing.

SensorWAN is not an interoperability protocol, and as such, does not implement
device discovery mechanisms like `Home Assistant MQTT device discovery`_ or
`Sparkplug`_ do.

Instead, it is primarily a convention for implementing telemetry data transport
subsystems, supported by corresponding reference implementations like `Kotori`_,
`Terkin MicroPython Datalogger`_, and `TerkinTelemetry C++`_.


********
Features
********

- **Real-world topology.**

  The channel address reflects the real-world topology, and is not obstructed by
  any technical details, similar to the Sparkplug B principle.

  This makes it easy to understand the topology of the sensor network, and to inspect
  the communication channels without further ado, and without much prior knowledge or
  technical assistance.

- **Freedom in topic design.**

  The four address components ``realm``, ``network``, ``group``, and ``name``, can be
  freely adjusted to fit the jargon and semantics of your application or data acquisition
  scenario, see also :ref:`sensorwan-address-examples`.

- **Infinite number of channels.**

  The "wide" addressing scheme allows to address an arbitrary number of channels,
  located at any level of the address hierarchy.

- **Semantic grouping of channels.**

  Without any need for a registry and corresponding machineries, you are able to quickly
  establish address conventions. For example, it is both sensible and advisable to use
  address prefixes like ``<realm>/testdrive`` for designating channels to be exclusively
  used for testing purposes.

- **Permission control.**

  Optionally, permission control can be established in a way coherent to channel
  addresses, where individual permissions can be adjusted according to the hierarchical
  levels of the network/channel topology, for example, by using MQTT topic ACLs.


***************
Channel address
***************

This section explains the four individual address components of the *SensorWAN
channel addressing scheme*, reflecting the data channel topology hierarchy.

::

    realm/network/group/name

Realm
=====

``realm`` is the designated **system channel root**, implemented as a channel address prefix.

It will be assigned by the operator of the data acquisition system. Operating multiple realms
on the topmost address level effectively implements system-level `multi-tenancy`_.

When using `Kotori`_, it will be configured within the server configuration files, and as such,
is a "fixed" address component.

Network
=======

``network`` is your **personal channel root**, it designates the unique **user/owner**
of the channel.

This identifier is used to separate channel groups, and to assign them to individual
users, effectively implementing user-level `multi-tenancy`_.

SensorWAN does not impose any restriction on the format of the ``network`` identifier.
For maximum uniqueness, use UUIDv4. For better readability, use a custom identifier.

Group
=====

The ``group`` identifier addresses the **channel group**. You can assign it as you like.

For example, you can group your channels by reflecting locations/sites of your sensor
nodes, or names of intermediary data concentrators/hubs/gateways.

Name
====

``name`` designates the channel name. For example, you can use it to reflect the
**device/node identifier**. Choose anything you like.

----

.. tip::

    In order to assign unique values as address components, you can generate them by using
    online or standalone programs, see :ref:`sensorwan-unique-identifiers`. In order to
    get a few ideas about possible topology address implementations, have a look at the
    :ref:`sensorwan-address-examples`.


************
Channel type
************

On the last segment of a fully qualified channel specifier, the addressing scheme adds
a suffix component, which designates the channel type. It can be used to discriminate
between uplink, downlink, and other message types.

Uplink messages
===============

Data uplink messages are received from a device. SensorWAN currently discriminates
between ``/data``- and ``/event``-type messages/suffixes.

Downlink messages
=================

For pushing downlink messages to devices, SensorWAN uses the ``/downlink`` path suffix.


.. _sensorwan-direct-addressing:

*****************
Direct addressing
*****************

With SensorWAN 3.0, two "direct" addressing schemes have been added, which can be used to
directly address channels and devices, either by using their identifiers as opaque labels,
or by encoding the channel topology differently than using a path-based scheme. For example,
the "dash" character can be used to separate topology fragments.

::

    # Addressing a device.
    <realm>/device/123e4567-e89b-12d3-a456-426614174000

    # Addressing a channel.
    <realm>/channel/<network>-<group>-<name>

Therefore, the ``channel`` and ``device`` labels became reserved identifiers within the
``network`` namespace.


********************************
Topology mapping and translation
********************************

The *SensorWAN channel addressing scheme* defines a few conventions how to transparently
map the channel address from the transport protocol domain to addressing schemes of
other backend systems, like storage components.

Databases
=========

For databases following the classic ``database`` -> ``table`` addressing scheme, or
corresponding variants, the topology mapping from a path-based topic may look like::

    SensorWAN address: <realm>/<network>/<group>/<name>
    Database name:     <realm>_<network>
    Table name:        <group>_<name>

Message buses
=============

For message bus systems following a path-based addressing scheme, the channel address usually
can be used 1:1 across system boundaries. On specific occasions, it makes sense to translate
topic identifiers to the syntax conventions used in downstream systems. For example, AMQP
usually encodes topic identifiers (here: routing keys) with fragments separated by dots. In
this case, a topic identifier mapping may look like::

    SensorWAN address: <realm>/<network>/<group>/<name>
    AMQP routing key:  <realm>.<network>.<group>.<name>

Object stores
=============

In S3, buckets and objects are the primary resources, and objects are stored in buckets.
S3 has a flat structure instead of a hierarchy like you would see in a file system.
However, for the sake of organizational simplicity, the folder concept is usually
synthesized as a means of grouping objects.

Building upon the SensorWAN path-based addressing scheme, a suitable object address within
an S3 bucket would be, for example, ``<realm>/<network>/<group>/<name>.parquet``.


***************
Payload formats
***************

SensorWAN does not impose any constraints on payload formats. You are free to select
anything which fits your needs. However, it provides a mechanism to convey content
type information over transport links which do not offer corresponding metadata fields,
like HTTP's ``Content-Type`` header.

For example, `MQTT`_ version 3 does not provide any means to signal the content type,
so the convention is to add the file extension of the corresponding format to the
channel type suffix.

For example, in a typical scenario where devices are submitting JSON data payloads
over MQTTv3 on the "data" channel, a corresponding full channel path specifier would
add a ``/data.json`` suffix to the channel base address.

::

    <realm>/<network>/<group>/<name>/data.json


********
Appendix
********

.. _sensorwan-address-examples:

Addressing examples
===================

To give you a few examples of possible addressing topologies for more specific use-cases:

- | **continent/country/region/city**
  | Addressing a global/world-wide scenario, or corresponding variants thereof.

- | **amazonas/ecuador/cuyabeno/hydro-1**
  | When looking at a more regional scenario instead. This is the canonical topology example we
  | are using on a few spots in the documentation of the reference implementations.

- | **organization/beekeeper/apiary/hive**
  | The data acquisition topology of the Hiveeyes project.

- | **organization/plant/shop-floor/machine**
  | For addressing industrial data acquisition scenarios.

.. _sensorwan-unique-identifiers:

Unique identifiers
==================

In order to assign unique values as address components, you can generate them by using
online or standalone programs.

For example, generate UUIDs, like ``34f83b61-9044-4ca8-b310-84f412175a4d`` using the
`Online UUID Generator`_, or generate UUIDs and other kinds of random identifiers more
suitable for human consumption using the `Vasuki`_ identifier generator, which you can
use on your own systems as either a command line program, or as a library.

.. tip::

    If you don't fancy UUIDs, and would like to use shorter identifiers instead, like ``re69x8``,
    or ``ZgBxoo``, saving bandwidth both on the wire and on human communication about them, we
    recommend to use *Nagamani19*. Nagamani19 is a short, unique, non-sequential identifier
    based on `Hashids`_ and a custom Epoch starting on January 1, 2019.

    For generating random, pronounceable pseudo-words like ``blaumaueff``, or ``schnoerr``,
    we recommend to use the *Gibberish* generator.

    Even shorter names, like ``Gime``, ``Togu``, or ``Viku``, suitable for assigning individual
    device names in a scenario with a few devices can be generated by using epoch slugs,
    available through the *MomentName* generator.


History
=======

The SensorWAN convention has originally been conceived on behalf of the Hiveeyes project.
In this context, and with its initial implementation as a channel address decoding
strategy for the `Kotori`_ data historian, it had different names, like »MQTT topic
addressing with a quadruple hierarchy strategy«, and later, just »MQTTKit«.

- Oct 19, 2015: Version 0.1 and 0.2 -- A `BERadio extension`_ for the `Hiveeyes One topology`_,
  defining the `Hiveeyes channel addressing`_.
- Mar 28, 2016: Version 1.0 -- Materialize as `Kotori's WanBusStrategy`_.
- Mar 9, 2020: Version 2.0 -- Document as :ref:`Kotori's MQTTKit application <application-mqttkit>`.
- Jun 6, 2023: Version 3.0 -- Naming things and direct-device addressing: :ref:`SensorWAN 3.0 <sensorwan-spec>`.


.. _BERadio extension: https://hiveeyes.org/docs/beradio/README.html#the-main-workhorse
.. _Hiveeyes channel addressing: https://hiveeyes.org/docs/system/acquisition/
.. _Hiveeyes One topology: https://hiveeyes.org/docs/system/vendor/hiveeyes-one/topology.html
.. _Kotori's WanBusStrategy: https://github.com/daq-tools/kotori/blob/main/kotori/daq/strategy/wan.py
.. _sensor node: https://en.wikipedia.org/wiki/Sensor_node
.. _sensor nodes: https://en.wikipedia.org/wiki/Sensor_node
.. _sensor network: https://en.wikipedia.org/wiki/Wireless_sensor_network
.. _sensor networks: https://en.wikipedia.org/wiki/Wireless_sensor_network

.. _Hashids: https://hashids.org/
.. _Home Assistant MQTT device discovery: https://www.home-assistant.io/integrations/mqtt/#mqtt-discovery
.. _multi-tenancy: https://en.wikipedia.org/wiki/Multitenancy
.. _Online UUID Generator: https://www.uuidgenerator.net/
.. _Sparkplug: https://sparkplug.eclipse.org/
.. _Terkin MicroPython Datalogger: https://github.com/hiveeyes/terkin-datalogger
.. _TerkinTelemetry: https://hiveeyes.org/docs/arduino/TerkinTelemetry/README.html
.. _TerkinTelemetry C++: https://hiveeyes.org/docs/arduino/TerkinTelemetry/README.html
.. _Vasuki: https://api.hiveeyes.org/vasuki/
