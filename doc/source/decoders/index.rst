.. include:: ../_resources.rst
.. include:: ../_meta.rst

.. _kotori-decoders:

########
Decoders
########

Decoders will know about device- or platform-specific payload formats
and will decode telemetry messages appropriately.
This documentation section is about the collection of decoders already
shipped with Kotori.

----

**************
Sonoff-Tasmota
**************

.. container:: pull-left width-50

    .. cssclass:: text-x-large

        People of `Raumfahrtagentur`_ are running the `Sonoff-Tasmota`_
        firmware on one of their `Sonoff SC`_ devices.

    .. cssclass:: text-larger

        The Sonoff SC is an environmental monitoring device for measuring
        current temperature, humidity, light intensity, air quality (particulates)
        and sound levels (noise pollution).

.. container:: pull-right

    .. figure:: https://ptrace.getkotori.org/2019-06-04_Sonoff-SC.jpg
        :alt: Sonoff SC: Environmental monitoring device
        :width: 300px
        :target: https://www.itead.cc/wiki/Sonoff_SC

        Sonoff SC: Environmental monitoring device

|clearfix|

.. container:: pull-left width-40

    .. figure:: https://ptrace.getkotori.org/2019-06-04_Sonoff-TH10-TH16.jpg
        :alt: Sonoff TH: Temperature and Humidity Monitoring WiFi Smart Switch
        :width: 300px
        :target: https://www.itead.cc/smart-home/sonoff-th.html

        Sonoff TH: Temperature and Humidity Monitoring WiFi Smart Switch

.. container:: pull-right width-60

    .. cssclass:: text-x-large

        Other devices running the Sonoff-Tasmota firmware and
        emitting telemetry information should work likewise.

    .. cssclass:: text-larger

        The Sonoff TH is an environmental monitoring and controlling device which
        can measuring current temperature and humidity.

|clearfix|


.. container:: pull-right

    .. container:: btn-outline text-x-large

        :ref:`Read all about the Tasmota Decoder... <decoder-tasmota>`

|clearfix|


----


