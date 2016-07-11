.. include:: _resources.rst

.. _kotori-about:

############
About Kotori
############

.. container:: pull-left basic-hero

    .. container:: align-center legroom-md

        Kotori is a multi-channel, multi-protocol data acquisition and graphing toolkit
        based on Grafana_, InfluxDB_, Mosquitto_ and Twisted_. It is written in Python.

.. container:: pull-right

    .. figure:: https://ptrace.isarengineering.de/2016-05-23_chart-recorder.png
        :alt: Chart recorder
        :width: 300px
        :align: left

|clearfix|


.. container:: pull-left

    .. raw:: html

        <a href="#">
            <span class="hb hb-md hb-kotori">
                <img src="_static/img/kotori-logo.png" style="width: 75px; margin-top: -15px"/>
            </span>
        </a>
        <a href="#">
            <span class="hb hb-md hb-kotori">
                <i class="fa fa-rss"></i>
            </span>
        </a>

.. container:: pull-right basic-hero

    .. container:: align-center legroom-md

        Use convenient software and hardware components for building
        telemetry solutions, test benches and sensor networks.
        Build upon a flexible data acquisition integration framework.
        Address all aspects of collecting and storing
        sensor data from a multitude of data sources and devices.

|clearfix|


.. container:: pull-left basic-hero

    .. container:: align-center legroom-md

        Deliver an instant-on experience by providing built-in sensor adapters,
        flexible configuration capabilities, durable database storage and
        unattended graph visualization out of the box.

    .. container:: pull-left margin-right-md

        .. figure:: _static/img/logo/arm-mbed-logo.svg
            :target: mbed_
            :alt: ARM® mbed™
            :width: 200px

            ARM® mbed™

        .. figure:: _static/img/logo/arduino-community-logo.svg
            :target: Arduino_
            :alt: Arduino
            :width: 200px

            Arduino

    .. container:: pull-left margin-right-md

        .. figure:: _static/img/logo/mosquitto-logo.png
            :target: Mosquitto_
            :alt: Mosquitto
            :width: 75px

            Mosquitto

        .. figure:: _static/img/logo/influxdb-logo.svg
            :target: InfluxDB_
            :alt: InfluxDB
            :width: 75px

            InfluxDB

        .. figure:: _static/img/logo/grafana-icon.png
            :target: Grafana_
            :alt: Grafana
            :width: 75px

            Grafana



    .. container:: pull-left

        .. figure:: _static/img/logo/twistedmatrix-logo.jpg
            :target: Twisted_
            :alt: Twisted
            :width: 100px

            Twisted

        .. figure:: _static/img/logo/crossbar-logo.svg
            :target: `Crossbar.io`_
            :alt: Crossbar.io
            :width: 150px

            Crossbar.io

        .. figure:: _static/img/logo/autobahn-logo.svg
            :target: Autobahn_
            :alt: Autobahn
            :width: 100px

            Autobahn


.. container:: pull-right

    .. raw:: html

        <a href="#">
            <span class="hb hb-md hb-google-plus">
                <i class="fa fa-plug"></i>
            </span>
        </a>
        <a href="#">
            <span class="hb hb-md hb-custom">
                <i class="fa fa-refresh"></i>
            </span>
        </a>

        <br/>

        <a href="#">
            <span class="hb hb-md hb-tumblr">
                <i class="fa fa-database"></i>
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


.. container:: pull-right basic-hero

    .. container:: align-center legroom-md

        Integrate with and extend your currently established
        measurement data acquisition workflow through flexible
        adapter interfaces to commodity or proprietary software
        and hardware components or protocols.


    .. container:: pull-left margin-right-md

        .. figure:: _static/img/logo/mqttorg-logo.svg
            :target: MQTT_
            :alt: MQTT
            :width: 200px

            MQTT

    .. container:: pull-right margin-right-md

        .. figure:: _static/img/logo/wamp-logo.svg
            :target: WAMP_
            :alt: WAMP
            :width: 200px

            WAMP


|clearfix|



.. _kotori-goals:

***************
Goals of Kotori
***************

The design of Kotori follows requirements from different audiences and use cases.

For all users
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
  such as TSDB, RDBMS or NoSQL.
- Rewrite and redistribute data through a variety of egress data channels.
- Instantly display measurement values on arrival using default database dashboards.
- Optionally, build advanced dashboards interactively.
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


.. container:: align-center basic-hero

    The search is over: :ref:`Kotori` is the lightweight and hackable
    SCADA_ system based on contemporary technologies and a solid foundation
    of open source software components you always have been looking for.


----


********
Appendix
********

Legal
=====

ARM® mbed™
----------
ARM is a registered trademark of ARM Limited (or its subsidiaries) in the EU and/or elsewhere.
mbed is a trademark of ARM Limited (or its subsidiaries) in the EU and/or elsewhere.
All rights reserved.

Arduino
-------
The Arduino brand and Arduino logo are copyright of Arduino LLC.
