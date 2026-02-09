.. _kotori-readme:

######
Kotori
######

.. container:: align-center

    .. figure:: https://ptrace.getkotori.org/2016-05-23_chart-recorder.png
        :alt: Chart recorder
        :width: 240px
        :target: .

    |

    *Telemetry data acquisition and sensor networks for humans.*

    .. image:: https://assets.okfn.org/images/ok_buttons/oc_80x15_blue.png
        :target: https://okfn.org/opendata/

    .. image:: https://assets.okfn.org/images/ok_buttons/ok_80x15_red_green.png
        :target: https://okfn.org/opendata/

    .. image:: https://assets.okfn.org/images/ok_buttons/os_80x15_orange_grey.png
        :target: https://okfn.org/opendata/

----

- **Status**:

  .. image:: https://github.com/daq-tools/kotori/workflows/Tests/badge.svg
        :target: https://github.com/daq-tools/kotori/actions?workflow=Tests
        :alt: CI outcome

  .. image:: https://codecov.io/gh/daq-tools/kotori/branch/main/graph/badge.svg
        :target: https://codecov.io/gh/daq-tools/kotori
        :alt: Test suite code coverage

  .. image:: https://img.shields.io/pypi/pyversions/kotori.svg
        :target: https://pypi.org/project/kotori/
        :alt: Supported Python versions

  .. image:: https://img.shields.io/pypi/v/kotori.svg
        :target: https://pypi.org/project/kotori/
        :alt: Package version on PyPI

  .. image:: https://img.shields.io/pypi/status/kotori.svg
        :target: https://pypi.org/project/kotori/
        :alt: Project status (alpha, beta, stable)

  .. image:: https://img.shields.io/pypi/l/kotori.svg
        :target: https://pypi.org/project/kotori/
        :alt: Project license

- **Usage**:

  .. image:: https://static.pepy.tech/personalized-badge/kotori?period=month&left_text=PyPI%20downloads%20%2F%20month&left_color=gray&right_color=orange
        :target: https://pepy.tech/project/kotori
        :alt: PyPI downloads per month

  .. image:: https://img.shields.io/docker/pulls/daqzilla/kotori.svg?label=docker%20pulls%20(kotori)
        :target: https://hub.docker.com/r/daqzilla/kotori
        :alt: Docker image pulls for `kotori` (total)

  .. image:: https://img.shields.io/docker/pulls/daqzilla/kotori-standard.svg?label=docker%20pulls%20(kotori-standard)
        :target: https://hub.docker.com/r/daqzilla/kotori-standard
        :alt: Docker image pulls for `kotori-standard` (total)

- **Compatibility**:

  .. image:: https://img.shields.io/badge/Mosquitto-1.5%2C%201.6%2C%202.0-blue.svg
        :target: https://github.com/eclipse/mosquitto
        :alt: Supported Mosquitto versions

  .. image:: https://img.shields.io/badge/Grafana-5.x%20--%2012.x-blue.svg
        :target: https://github.com/grafana/grafana
        :alt: Supported Grafana versions

  .. image:: https://img.shields.io/badge/InfluxDB-1.6%2C%201.7%2C%201.8-blue.svg
        :target: https://github.com/influxdata/influxdb
        :alt: Supported InfluxDB versions

  .. image:: https://img.shields.io/badge/MongoDB-3.x%20--%207.x-blue.svg
        :target: https://github.com/mongodb/mongo
        :alt: Supported MongoDB versions


----


*****
About
*****

Kotori is a multi-channel, multi-protocol telemetry data acquisition and graphing
toolkit for `time-series`_ data processing.

It supports a variety of scenarios in scientific environmental monitoring projects,
for building and operating distributed sensor networks, and for industrial data
acquisition applications.


Details
=======

Kotori takes the role of the `data historian`_ component within a `SCADA`_ / `MDE`_
system, exclusively built upon industry-grade `free and open-source software`_
like Grafana_, Mosquitto_, or InfluxDB_. It is written in Python_,
and uses the Twisted_ networking library.

The best way to find out what you can do with Kotori, is by looking at
some outlined `scenarios`_ and by reading how others are using it at the
`example gallery <gallery_>`_. To learn more about the technical details, have
a look at the used `technologies`_.


Features
========

- Multi-channel and multi-protocol data-acquisition and -storage. Collect and
  store sensor data from different kinds of devices, data sources, and protocols.
- Built-in sensor adapters, flexible configuration capabilities, durable
  database storage and unattended graph visualization.
- Based on an infrastructure toolkit assembled from different components
  suitable for data-acquisition, -storage, -fusion, -graphing and more.
- Leverage the flexible data acquisition integration framework for building
  telemetry data acquisition and logging systems, test benches, or sensor
  networks for environmental monitoring systems, as well as other kinds of
  data-gathering and -aggregation projects.
- It integrates well with established hardware-, software- and
  data acquisition workflows through flexible adapter interfaces.


************
Installation
************

Kotori can be installed in different ways. You may prefer using a Debian
package, install it from the Python Package Index (PyPI), or run it within
a `development sandbox`_ directly from the Git repository.

Corresponding installation instructions are bundled at
https://getkotori.org/docs/setup/.


********
Synopsis
********

A compact example how to submit measurement data on a specific channel, using
MQTT and HTTP, and export it again.

Data acquisition
================

First, let's define a data acquisition channel::

    CHANNEL=amazonas/ecuador/cuyabeno/1

and some example measurement data::

    DATA='{"temperature": 42.84, "humidity": 83.1}'

Submit with MQTT::

    MQTT_BROKER=daq.example.org
    echo "$DATA" | mosquitto_pub -h $MQTT_BROKER -t $CHANNEL/data.json -l

Submit with HTTP::

    HTTP_URI=https://daq.example.org/api/
    echo "$DATA" | curl --request POST --header 'Content-Type: application/json' --data @- $HTTP_URI/$CHANNEL/data

Data export
===========
Measurement data can be exported in a variety of formats.

This is a straight-forward example for CSV data export::

    http $HTTP_URI/$CHANNEL/data.csv


****************
Acknowledgements
****************

Thanks a stack to all the `contributors`_ who helped to co-create and conceive
Kotori in one way or another. You know who you are.


*******************
Project information
*******************

Contributions
=============

Every kind of contribution, feedback, or patch, is much welcome. `Create an
issue`_ or submit a patch if you think we should include a new feature, or to
report or fix a bug.

Development
===========

In order to setup a development environment on your workstation, please head over
to the `development sandbox`_ documentation. When you see the software tests succeed,
you should be ready to start hacking.

Resources
=========

- `Source code <https://github.com/daq-tools/kotori>`_
- `Documentation <https://getkotori.org/>`_
- `Python Package Index (PyPI) <https://pypi.org/project/kotori/>`_

License
=======

The project is licensed under the terms of the GNU AGPL license, see `LICENSE`_.


************
Supported by
************

.. image:: https://resources.jetbrains.com/storage/products/company/brand/logos/jetbrains.svg
    :target: https://jb.gg/OpenSourceSupport

Special thanks to the people at JetBrains s.r.o. for supporting us with
excellent development tooling.


.. _Autobahn: https://crossbar.io/autobahn/
.. _contributors: https://getkotori.org/docs/project/contributors.html
.. _Create an issue: https://github.com/daq-tools/kotori/issues/new
.. _data historian: https://en.wikipedia.org/wiki/Operational_historian
.. _development sandbox: https://getkotori.org/docs/setup/sandbox.html
.. _free and open-source software: https://en.wikipedia.org/wiki/Free_and_open-source_software
.. _gallery: https://getkotori.org/docs/gallery/
.. _Grafana: https://en.wikipedia.org/wiki/Grafana
.. _InfluxDB: https://en.wikipedia.org/wiki/InfluxDB
.. _LICENSE: https://github.com/daq-tools/kotori/blob/main/LICENSE
.. _MDE: https://de.wikipedia.org/wiki/Maschinendatenerfassung
.. _MongoDB: https://en.wikipedia.org/wiki/MongoDB
.. _Mosquitto: https://github.com/eclipse/mosquitto
.. _MQTT: https://en.wikipedia.org/wiki/MQTT
.. _Python: https://www.python.org/
.. _SCADA: https://en.wikipedia.org/wiki/SCADA
.. _scenarios: https://getkotori.org/docs/about/scenarios.html
.. _technologies: https://getkotori.org/docs/about/technologies.html
.. _time-series: https://en.wikipedia.org/wiki/Time_series
.. _Twisted: https://en.wikipedia.org/wiki/Twisted_(software)
