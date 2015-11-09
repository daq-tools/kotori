.. Kotori documentation master file, created by
   sphinx-quickstart on Fri Nov  6 21:36:37 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Kotori!
==================

*Kotori* is a multi-channel, multi-protocol data acquisition and graphing toolkit based on
InfluxDB_, Grafana_, Mosquitto_, Twisted_ and Autobahn_.

Being a convenient component for building telemetry solutions and test benches, it addresses different aspects of collecting
and storing sensor data from a multitude of data sources and devices.

.. _InfluxDB: https://influxdb.com/
.. _Grafana: http://grafana.org/
.. _Twisted: https://twistedmatrix.com/
.. _Mosquitto: http://mosquitto.org/
.. _Autobahn: http://autobahn.ws/


About
-----

.. toctree::
    :maxdepth: 1

    README


Applications
------------

.. toctree::
    :maxdepth: 1
    :glob:

    applications/*


Setup
-----

.. toctree::
    :maxdepth: 1
    :glob:

    setup/*


Development
-----------

.. toctree::
    :maxdepth: 1
    :glob:

    development/index
    changes


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

