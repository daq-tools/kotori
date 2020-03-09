.. _kotori-readme:

######
Kotori
######

.. container:: align-center

    .. image:: https://assets.okfn.org/images/ok_buttons/ok_80x15_red_green.png
        :target: https://okfn.org/opendata/

    .. image:: https://assets.okfn.org/images/ok_buttons/oc_80x15_blue.png
        :target: https://okfn.org/opendata/

    .. image:: https://assets.okfn.org/images/ok_buttons/os_80x15_orange_grey.png
        :target: https://okfn.org/opendata/

    |

    .. figure:: https://ptrace.getkotori.org/2016-05-23_chart-recorder.png
        :alt: Chart recorder
        :width: 300px

    *Telemetry data acquisition and sensor networks for humans.*

----

**Documentation**: https://getkotori.org/

**Source Code**: https://github.com/daq-tools/kotori/

**Status**:

.. image:: https://img.shields.io/badge/Python-2.7-green.svg
    :target: https://github.com/daq-tools/kotori

.. image:: https://img.shields.io/pypi/v/kotori.svg
    :target: https://pypi.org/project/kotori/

.. image:: https://img.shields.io/github/tag/daq-tools/kotori.svg
    :target: https://github.com/daq-tools/kotori


----


At a glance
===========
Kotori is a data historian based on InfluxDB, Grafana, MQTT and more. Free, open, simple.

It is a telemetry data acquisition, `time series`_ data processing and graphing toolkit
aiming to become a fully integrated `data historian`_.
It supports scientific environmental monitoring projects,
distributed sensor networks and likewise scenarios.

The best way to find out more about Kotori is by looking at how others use it already.
Enjoy reading about some `examples <https://getkotori.org/docs/examples/>`_ where Kotori has been used.

.. _time series: https://en.wikipedia.org/wiki/Time_series
.. _data historian: https://en.wikipedia.org/wiki/Operational_historian

Features
========
The key features are:

- Multi-channel and multi-protocol data-acquisition and -storage.
- Built-in sensor adapters, flexible configuration capabilities, durable
  database storage and unattended graph visualization out of the box.
- Based on an infrastructure toolkit assembled from different components
  suitable for data-acquisition, -storage, -fusion, -graphing and more.
- The system is used for building flexible telemetry solutions in different
  scenarios. It has been used to support conceiving data logging systems,
  test benches, sensor networks for environmental monitoring as well as other
  data-gathering and -aggregation projects.
- It integrates well with established hardware-, software- and
  data acquisition workflows through flexible adapter interfaces.

Technologies
============
Kotori is based on a number of fine infrastructure components and
technologies and supports a number of protocols in one way or another.
Standing on the shoulders of giants.

- Infrastructure: Mosquitto_, Grafana_, InfluxDB_, MongoDB_
- Runtime: Twisted_, Autobahn_
- Protocols: MQTT, HTTP, TCP, UDP, WebSockets, WAMP.

.. _Twisted: https://en.wikipedia.org/wiki/Twisted_(software)
.. _Mosquitto: https://github.com/eclipse/mosquitto
.. _Grafana: https://github.com/grafana/grafana
.. _Autobahn: https://autobahn.readthedocs.io/
.. _InfluxDB: https://github.com/influxdata/influxdb
.. _MongoDB: https://github.com/mongodb/mongo


************
Installation
************
Kotori can be installed through a Debian package, from the
Python Package Index (PyPI) or from the Git repository.
Please follow up to the corresponding installation instructions:

https://getkotori.org/docs/setup/


********
Examples
********
Data acquisition is easy, both MQTT and HTTP are supported.

MQTT::

    CHANNEL_TOPIC=amazonas/ecuador/cuyabeno/1/data.json
    mosquitto_pub -t $CHANNEL_TOPIC -m '{"temperature": 42.84, "humidity": 83.1}'

HTTP::

    CHANNEL_URI=http://localhost:24642/api/amazonas/ecuador/cuyabeno/1/data
    echo '{"temperature": 42.84, "humidity": 83.1}' | curl --request POST --header 'Content-Type: application/json' --data @- $CHANNEL_URI


****************
Acknowledgements
****************
Thanks to all the `contributors <https://getkotori.org/docs/project/contributors.html>`_
who helped to co-create and conceive Kotori in one way or another. You know who you are.


*******
License
*******
This project is licensed under the terms of the AGPL license.
