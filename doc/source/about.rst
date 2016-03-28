.. include:: _resources.rst

############
About Kotori
############

    *Kotori* is a multi-channel, multi-protocol data acquisition and graphing toolkit
    based on InfluxDB_, Grafana_, Mosquitto_ and Twisted_.

    It is a convenient component for building flexible telemetry solutions, test benches
    and sensor networks by addressing different aspects of collecting and storing sensor
    data from a multitude of data sources and devices.

***********
At a glance
***********
The big picture of the data acquisition integration framework is a system aiming to:

.. container:: pull-left basic-hero align-center

    Deliver an instant-on experience by providing built-in sensor adapters,
    flexible configuration capabilities, durable database storage and
    unattended graph visualization out of the box.

.. container:: pull-right

    .. raw:: html

        <a href="#">
            <span class="hb hb-md hb-google-plus">
                <i class="fa fa-plug"></i>
            </span>
        </a>
        <a href="#">
            <span class="hb hb-md hb-linkedin">
                <i class="fa fa-signal"></i>
            </span>
        </a>

|clearfix|


.. container:: pull-left

    .. raw:: html

        <a href="#">
            <span class="hb hb-md hb-xing">
                <i class="fa fa-gears"></i>
            </span>
        </a>
        <a href="#">
            <span class="hb hb-md hb-tencent-weibo">
                <i class="entypo flow-tree"></i>
            </span>
        </a>

.. container:: pull-right basic-hero align-center

    Integrate well with and extend your currently employed
    measurement data acquisition workflow through flexible
    adapter interfaces to commodity or proprietary software
    and hardware components.


|clearfix|


.. container:: align-center basic-hero


.. raw:: html



***************
Goals of Kotori
***************

The design of Kotori has different audiences in mind.

For all users
=============
:ref:`Kotori` takes the burden of manually recording and carrying
measurement and telemetry data around off your shoulders.
A quick overview should get you an idea:

- Ingest data using open or proprietary industry protocols and standards.
- Collect measurement data from wired or wireless sensors.
- Persist measurement data into contemporary databases and storage systems.
- Instantly display measurement values on arrival using default database dashboards.
- Optionally, build advanced dashboards interactively.

----

- receive data from various types of ingress data channels: MQTT, UDP, HTTP
- store collected data into different kinds of databases: TSDB, RDBMS, NoSQL
- convert and transcode data from/to different payload formats: CSV, JSON, XML, etc.
- rewrite and redistribute data through a variety of egress data channels
- display measurement data in rich database dashboards
- notify subscribed users or devices of events like above-/below-threshold



For integrators
===============
:ref:`Kotori` supports you in

- building field solutions like receiving telemetry data transmitted
  from vehicles and moving objects as done in the pilot project with the
  University of Applied Sciences in Munich.
  This was about collecting and visualizing telemetry data and
  position information from a fuel-cell powered vehicle when racing
  at the Shell Ecomarathon 2015 in Rotterdam.
  See also :ref:`vendor-hydro2motion`.

- building distributed data collector platforms like the
  sensor data network for a Berlin-based beekeeper collective.
  See also :ref:`vendor-hiveeyes`.

- setting up maintenance-free measurement data collectors at your
  laboratory or test bench using established customer-specific
  communication protocols.
  See also :ref:`vendor-lst`.


.. container:: align-center basic-hero

    To get an idea about the diversity of use cases, have a look at
    the different areas and scopes of integration scenarios
    collected at :ref:`Kotori Applications <kotori-applications>`.


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
- Listen and talk M2M_ using the *MQ Telemetry Transport* connectivity protocol (MQTT_).
- Store data points into InfluxDB_, a leading open source time series database suitable
  for realtime analytics and sensor data storage.
- Automate dashboard management in the context of data arriving on different data channels
  using Grafana_, an open source, feature rich metrics dashboard and graph editor.
- Make Browser clients first-class citizens of the underpinning software bus framework
  delivering bidirectional communication with publish/subscribe or rpc semantics
  using the *Web Application Messaging Protocol* (WAMP_), in turn based on WebSockets_.
- Integration with mqttwarn_ for emitting and broadcasting data to a multitude of targets and receivers.
- Accept new protocols, write adapters, decoders and handlers for specific devices, data formats
  and databases.


.. container:: align-center basic-hero

    The search is over: :ref:`Kotori` is the lightweight and hackable
    SCADA_ system based on contemporary technologies and a large foundation of
    open source software components you have always been waiting for.
