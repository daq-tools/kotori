.. include:: ../../_resources.rst

.. _airrohr-decoder:

###############
Airrohr decoder
###############


*****
About
*****
Ingest telemetry data from air particulate measurement devices of the
`Sensor.Community`_ (formerly `Luftdaten.Info`_) project running the
`Airrohr Firmware`_.


*********
Appliance
*********
.. figure:: https://ptrace.getkotori.org/2020-03-12_airrohr-appliance.png
    :target: https://ptrace.getkotori.org/2020-03-12_airrohr-appliance.png
    :alt: The Airrohr appliance
    :width: 350px

The sensor appliance is based on an ESP8266. It supports the SPS30, SDS011,
DHT22, BMP180, BMP/E 280, NEO-6M sensors and many more.

The system can submit measurement data to different sinks in various formats
(Sensor.Community, Madavi, OpenSenseMap, AirCMS, InfluxDB, CSV)
and also a custom HTTP API endpoint.


*************
Configuration
*************
Getting the system configured properly is important,
please read this section carefully.

.. figure:: https://ptrace.getkotori.org/2020-03-12_airrohr-configuration.png
    :target: https://ptrace.getkotori.org/2020-03-12_airrohr-configuration.png
    :alt: Airrohr custom API configuration
    :width: 350px

    Airrohr custom API configuration


Settings
========
Let's imagine a communication channel address and a device identifier.

| **Channel**: ``universe/milky-way/earth-one``
| **Device**: ``node-42``

The appropriate settings for the Airrohr settings dialog would then be

| **Server**: ``daq.example.org``
| **Path**: ``/api-notls/universe/milky-way/earth-one/node-42/custom/airrohr``
| **Port**: ``80``

Please note the ``/custom/airrohr`` suffix here.


*******
Example
*******
Submit an example JSON message payload to the HTTP API::

    http https://raw.githubusercontent.com/daq-tools/kotori/master/doc/source/handbook/decoders/airrohr.json \
        | http POST http://daq.example.org/api-notls/universe/milky-way/earth-one/node-42/custom/airrohr

The payload will be forwarded to this MQTT topic::

    universe/milky-way/earth-one/node-42/custom/airrohr.json
