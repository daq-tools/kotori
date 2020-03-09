.. include:: ../_resources.rst


.. _kotori-technologies:

************
Technologies
************

Introduction
============
DaqZilla is currently made of these free and open source software components:

- :ref:`Kotori`, a data acquisition, graphing and telemetry toolkit
- Grafana_, a graph and dashboard builder for visualizing time series metrics
- InfluxDB_, a time-series database
- Mosquitto_, a MQTT message broker
- MongoDB_, a document store (optional) ¹²

| ¹ MongoDB is only required when doing CSV data acquisition, so it is completely
| optional for regular operations of Kotori.
| ² As MongoDB - strictly speaking - stopped being free software recently (2018/2019),
| it will probably be phased out gradually and replaced by PostgreSQL.


Overview
========

.. container:: pull-left basic-hero

    .. container:: align-center legroom-md

        Deliver an instant-on experience by providing built-in sensor adapters,
        flexible configuration capabilities, durable database storage and
        unattended graph visualization out of the box.

    .. container:: pull-left margin-right-md

        .. figure:: ../_static/img/logo/arm-mbed-logo.svg
            :target: mbed_
            :alt: ARM® mbed™
            :width: 200px

            ARM® mbed™

        .. figure:: ../_static/img/logo/arduino-community-logo.svg
            :target: Arduino_
            :alt: Arduino
            :width: 200px

            Arduino

    .. container:: pull-left margin-right-md

        .. figure:: ../_static/img/logo/mosquitto-logo.png
            :target: Mosquitto_
            :alt: Mosquitto
            :width: 75px

            Mosquitto

        .. figure:: ../_static/img/logo/influxdb-logo.svg
            :target: InfluxDB_
            :alt: InfluxDB
            :width: 75px

            InfluxDB

        .. figure:: ../_static/img/logo/grafana-icon.png
            :target: Grafana_
            :alt: Grafana
            :width: 75px

            Grafana



    .. container:: pull-left

        .. figure:: ../_static/img/logo/twistedmatrix-logo.jpg
            :target: Twisted_
            :alt: Twisted
            :width: 100px

            Twisted

        .. figure:: ../_static/img/logo/crossbar-logo.svg
            :target: `Crossbar.io`_
            :alt: Crossbar.io
            :width: 150px

            Crossbar.io

        .. figure:: ../_static/img/logo/autobahn-logo.svg
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

        .. figure:: ../_static/img/logo/mqttorg-logo.svg
            :target: MQTT_
            :alt: MQTT
            :width: 200px

            MQTT

    .. container:: pull-right margin-right-md

        .. figure:: ../_static/img/logo/wamp-logo.svg
            :target: WAMP_
            :alt: WAMP
            :width: 200px

            WAMP


|clearfix|


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
