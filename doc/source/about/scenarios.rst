.. include:: ../_resources.rst


.. _kotori-goals:
.. _kotori-scenarios:

*********
Scenarios
*********

The design of Kotori follows requirements from different audiences and use cases.

.. container:: align-center basic-hero

    To get an idea about the diversity of use cases, have a look at
    the different areas and scopes of integration scenarios
    collected at :ref:`Kotori Examples <kotori-examples>`.

For consumers
=============
:ref:`Kotori` streamlines the process of collecting, storing,
visualizing and postprocessing measurement and telemetry data.
Forget about ad-hoc setups for recording data followed up by
custom postprocessing steps often involving tedious manual
transport-, conversion- and import-tasks.

A quick overview should get you an idea:

- Receive and ingest measurement data using open or proprietary
  industry protocols and standards such as MQTT_, UDP or HTTP.
- Collect measurement data from wired or wireless sensors and interfaces.
- Convert and transcode measurement data from/to different payload formats
  such as CSV, JSON, XML, etc.
- Persist measurement data into contemporary databases and storage systems
  such as TSDB, RDBMS or NoSQL without further ado.
- Rewrite and redistribute data through a variety of egress data channels.
- Instantly display measurement values on arrival using default database dashboards.
- Build advanced dashboards interactively using Grafana_.
- Notify subscribed users or devices of events like above-/below-threshold or data-loss.


For integrators
===============
:ref:`Kotori` is a toolbox for creating vendor solutions in different areas:

- Build field systems receiving telemetry data transmitted from vehicles
  and moving objects like in the pilot project :ref:`vendor-hydro2motion`,
  carried out with the University of Applied Sciences in Munich.
  This was about collecting and visualizing telemetry data and
  position information from a fuel-cell powered vehicle while
  being on-track at the Shell Ecomarathon 2015 in Rotterdam.

- Create distributed data collector platforms like :ref:`vendor-hiveeyes`,
  the sensor data collection network for a Berlin-based beekeeper collective.

- Integrate a maintenance-free measurement data collector into
  the toolbox at your laboratory or test bench setup.
  Adapts seamlessly to your local environment by reusing or
  interfacing with established on-site or customer-specific
  communication protocols and hardware.
  :ref:`vendor-lst` uses Kotori for collecting and decoding
  binary payloads of their in-house telemetry system.


For developers
==============
:ref:`Kotori` is built upon a powerful service composition framework.
Its goals are making it convenient for developers to ingest, emit
and distribute data between different data sources and data sinks,
and to transcode payloads between different formats.
It ships with built-in adapters to different popular software bus-
and storage-systems. Batteries included.

We are standing on the shoulders of giants:

- Leverage the open infrastructure based on Twisted_ - an event-driven networking engine -
  to implement custom software components.
- Listen and talk M2M_ using the *MQ Telemetry Transport* connectivity protocol and software bus (MQTT_).
- Store data points into InfluxDB_, a leading open source time series database suitable
  for realtime analytics and sensor data storage.
- Automate dashboard management in the context of data arriving on different data channels
  using Grafana_, an open source, feature rich metrics dashboard and graph editor.
- Make Browser clients first-class citizens of the underpinning software bus framework
  delivering bidirectional communication with publish/subscribe or rpc semantics
  using the Autobahn_ implementation of the *Web Application Messaging Protocol* (WAMP_),
  which in turn is based on WebSockets_.
- Integrate with mqttwarn_ for emitting and broadcasting data to a multitude of targets and receivers.
- Accept new protocols, write adapters, decoders and handlers for specific devices, data formats
  and databases.
- A lightweight and hackable SCADA_ system based on contemporary technologies and a
  solid foundation of open source software components you always have been looking for.
