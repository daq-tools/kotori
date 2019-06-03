.. image:: https://img.shields.io/badge/Python-2.7-green.svg
    :target: https://github.com/daq-tools/kotori

.. image:: https://img.shields.io/pypi/v/kotori.svg
    :target: https://pypi.org/project/kotori/

.. image:: https://img.shields.io/github/tag/daq-tools/kotori.svg
    :target: https://github.com/daq-tools/kotori

.. image:: https://assets.okfn.org/images/ok_buttons/od_80x15_red_green.png
    :target: https://okfn.org/opendata/

.. image:: https://assets.okfn.org/images/ok_buttons/oc_80x15_blue.png
    :target: https://okfn.org/opendata/

.. image:: https://assets.okfn.org/images/ok_buttons/os_80x15_orange_grey.png
    :target: https://okfn.org/opendata/

|

.. _kotori-readme:

**Telemetry data acquisition and sensor networks for humans.**

######
Kotori
######

Kotori is a flexible data historian based on InfluxDB, Grafana, MQTT and more. Free, open, simple.

It is a telemetry data acquisition, `time series`_ data processing and graphing toolkit
aiming to become a fully integrated `data historian`_.
It is being conceived to support scientific environmental monitoring
through distributed sensor networks and likewise scenarios.


.. _time series: https://en.wikipedia.org/wiki/Time_series
.. _data historian: https://en.wikipedia.org/wiki/Operational_historian


.. contents:: Table of Contents
   :local:
   :depth: 1

----


*************
In a nutshell
*************

About
=====
- Kotori is a multi-channel and multi-protocol data historian.
- It's an infrastructure toolkit assembled from different components
  suitable for data-acquisition, -storage, -fusion, -graphing and more.
- The system is used for building flexible telemetry solutions in different
  scenarios.
- It has been used to support conceiving data logging systems, test benches,
  sensor networks for environmental monitoring and beyond as well as other
  data-gathering and -aggregation projects.
- The system features a number of built-in sensor adapters, flexible configuration
  capabilities, durable database storage and unattended graph visualization out of the box.
- It integrates well with established hardware-, software- and
  data acquisition workflows through flexible adapter interfaces.

Explore
=======
It's best to find out more about Kotori by looking at how others use it already. Enjoy reading.

- Get a rough idea at `About Kotori <https://getkotori.org/docs/about.html>`_.
- Have a look at some `Applications <https://getkotori.org/docs/applications/>`_ where Kotori has been used.
- There are handbooks about `data acquisition <https://getkotori.org/docs/handbook/acquisition/>`_ and
  `data export <https://getkotori.org/docs/handbook/export/>`_.

Technologies
============
Kotori is based on a number of fine infrastructure components and technologies
and supports a number of protocols in one way or another.
Standing on the shoulders of giants.

- Infrastructure: Twisted_, Mosquitto_, Grafana_, InfluxDB_, Autobahn_, MongoDB_
- Protocols: MQTT, HTTP, TCP, UDP, WebSockets, WAMP

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

- `Packages for Debian-based distributions <https://getkotori.org/docs/setup/debian-quickstart.html>`_ ¹ ²
- `Installing Python source package <https://getkotori.org/docs/setup/python-package.html>`_
- `Installing from Git <https://getkotori.org/docs/development/hack.html>`_

As Kotori is pretty heavy in respect to the number of software
components it relies on, things sometimes break when trying to
install its dependencies.
In order to let us know about any problems you might encounter when
installing Kotori, please don't hesitate to
`open an issue on GitHub <https://github.com/daq-tools/kotori/issues/new>`_.

----

¹ When choosing to install from the Debian package repository, you will also be
able to receive appropriate Debian packages for Mosquitto, InfluxDB and Grafana
through the `DaqZilla package repository <https://packages.elmyra.de/elmyra/foss/debian/>`_.
This makes it easy to setup the complete DAQ system from a single package source.

² All of the Debian packages are available for ``amd64`` and ``armhf``
architectures to support installations on RaspberryPi, Beaglebone,
Odroid or similar ARM-based SBC machines.


****************
Acknowledgements
****************
Thanks to all the `contributors <https://getkotori.org/docs/CONTRIBUTORS.html>`_ of Kotori
who got their hands dirty with it and helped to co-create and conceive it
in one way or another. You know who you are.


*******************
Project information
*******************

About
=====
These links will guide you to the source code of »Kotori« and its documentation.

- `Kotori on GitHub <https://github.com/daq-tools/kotori>`_
- `Kotori documentation <https://getkotori.org/docs/>`_
- `Kotori on the Python Package Index (PyPI) <https://pypi.org/project/kotori/>`_

Contributing
============
We are always happy to receive code contributions, ideas, suggestions
and problem reports from the community.

So, if you'd like to contribute you're most welcome.
Spend some time taking a look around, locate a bug, design issue or
spelling mistake and then send us a pull request or create an issue_.

Thanks in advance for your efforts, we really appreciate any help or feedback.

Licenses
========
This software is copyright © 2013-2019 The Kotori Developers. All rights reserved.

It is and will always be **free and open source software**.

Use of the source code included here is governed by the
`GNU Affero General Public License <GNU-AGPL-3.0_>`_ and the
`European Union Public License <EUPL-1.2_>`_.
Please also have a look at the `notices about licenses of third-party components`_.

.. _issue: https://github.com/daq-tools/kotori/issues/new
.. _GNU-AGPL-3.0: https://github.com/daq-tools/kotori/blob/master/LICENSE
.. _EUPL-1.2: https://github.com/daq-tools/kotori/blob/master/eupl-1.2.txt
.. _notices about licenses of third-party components: https://github.com/daq-tools/kotori/blob/master/THIRD-PARTY-NOTICES.rst


***************
Troubleshooting
***************
If you encounter any problems during setup or operations or if you have further
suggestions, please let us know by `opening an issue on GitHub <https://github.com/daq-tools/kotori/issues/new>`_
or drop us a line at ``support@getkotori.org``. Thanks already.


.. note::

    If not already reading here, you might want to
    `continue reading on Kotori's documentation space <https://getkotori.org/docs/>`_.

----

Have fun!
