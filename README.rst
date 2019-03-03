.. image:: https://img.shields.io/badge/Python-2.7-green.svg
    :target: https://github.com/daq-tools/kotori

.. image:: https://img.shields.io/pypi/v/kotori.svg
    :target: https://pypi.org/project/kotori/

.. image:: https://img.shields.io/github/tag/daq-tools/kotori.svg
    :target: https://github.com/daq-tools/kotori

|


.. _kotori-readme:

**Telemetry data acquisition and sensor networks for humans.**


######
Kotori
######

Kotori is a flexible data historian based on InfluxDB, Grafana, MQTT and more. Free, open, simple.

It is a telemetry data acquisition, processing and graphing toolkit
aiming to become a fully integrated data historian.
It is being conceived to support scientific environmental monitoring
through distributed sensor networks and likewise scenarios.


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

- It's an infrastructure toolkit made of components for data acquisition, graphing and more.

- The system is used for building flexible telemetry solutions in different scenarios.

    - Test benches
    - Sensor networks
    - Environmental monitoring

- Built-in sensor adapters, flexible configuration capabilities,
  durable database storage and unattended graph visualization out of the box.

- Integrates well with established hardware-, software- and
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
Kotori can be installed through a Debian package and from PyPI.
Our Debian package repository also contains appropriate packages
for Mosquitto, InfluxDB and Grafana, so this should get up the
whole DAQ infrastructure in a few minutes.

All of the packages are available for ``amd64`` and ``armhf``
architectures to support installations on RaspberryPi, Beaglebone,
Odroid or similar ARM-based SBC machines.

Please follow up to the corresponding installation instructions:

- `Packages for Debian-based distributions <https://getkotori.org/docs/setup/debian-quickstart.html>`_
- `Python source packages <https://getkotori.org/docs/setup/python-package.html>`_

As Kotori is pretty heavy in respect to the number of software
components it relies on, things sometimes break here.

In order to let us know about any problems you might encounter when
installing Kotori, please don't hesitate to open an issue on GitHub.


****************
Acknowledgements
****************
Kotori would not have been possible without many amazing people:

- Glyph Lefkowitz et al. for conceiving, building and maintaining the
  Twisted network programming framework.
- Roger Light et al. for conceiving, building and maintaining the
  Mosquitto MQTT broker.
- Torkel Ödegaard and his team for creating and maintaining Grafana.
- Paul Dix and his team for creating and maintaining InfluxDB.
- The PostgreSQL and MongoDB developers for creating and maintaining
  their database systems.
- Chris McDonough and the whole Python Webdev community for creating
  and maintaining the Pyramid and Pylons ecosystems.
- Tobias Oberstein et al. for creating and maintaining WAMP,
  Crossbar.io and Autobahn.
- Countless other authors of packages from the Python
  ecosystem and beyond for adding even more batteries
  to put everything together.

Thank you so much for providing such great infrastructure
components and resources to the community!
You know who you are.

Last but not least, thanks to all the
`core contributors <https://getkotori.org/docs/CONTRIBUTORS.html>`_ of Kotori
who got their hands dirty with it and helped to co-create and conceive it
in one way or another.


*******************
Project information
*******************

About
=====
The source code of Kotori is hosted on `GitHub <https://github.com/daq-tools/kotori>`_.
You might also want to have a look at the `documentation <https://getkotori.org/docs/>`_.

If you'd like to contribute you're most welcome!
Spend some time taking a look around, locate a bug, design issue or
spelling mistake and then send us a pull request or create an issue.

Thanks in advance for your efforts, we really appreciate any help or feedback.

Licensing
=========
- The source code is primarily licensed under the terms of the
  GNU AGPL license, see LICENSE_ file for details.
- The program is also licensed under the terms of the
  European Union Public Licence (EUPL 1.2, see file "eupl-1.2.txt").
- The program also includes third-party components from different authors,
  see "THIRD-PARTY-NOTICES.rst" for more information on that.

.. _LICENSE: https://github.com/daq-tools/kotori/blob/master/LICENSE


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
