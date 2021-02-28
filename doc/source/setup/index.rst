.. include:: ../_resources.rst

.. _kotori-setup:

#####
Setup
#####


************
Introduction
************

Kotori can be installed through a Debian package ¹², by using Docker images
from Docker Hub, from the Python Package Index (PyPI) or from the Git
repository.

For running Kotori in a full configuration, you will need some other
infrastructure services like Mosquitto_, InfluxDB_, Grafana_ and optionally
MongoDB_.

Have fun and enjoy your data acquisition!


*******
Details
*******

.. toctree::
    :caption: Baseline setup
    :maxdepth: 1

    linux-debian
    linux-arch
    docker
    macos
    python-package


.. toctree::
    :caption: Production setup
    :maxdepth: 1

    security
    nginx


.. toctree::
    :caption: Development
    :maxdepth: 1

    sandbox
    troubleshooting


----


¹ When choosing to install from the Debian package repository, you will also be
able to receive appropriate Debian packages for Mosquitto, InfluxDB and Grafana
through the `DaqZilla package repository <https://packages.elmyra.de/elmyra/foss/debian/>`_.
This makes it easy to setup the complete DAQ system from a single package source.

² All of the Debian packages are available for ``amd64`` and ``armhf``
architectures to support installations on RaspberryPi, Beaglebone,
Odroid or similar ARM-based SBC machines.


***************
Troubleshooting
***************

Some effort has been done to make the installation process of Kotori and
associated software components as easy and straight forward as possible.

However, things go south sometimes so there might still be rough edges we would
love to learn about. So, please don't hesitate to drop us a note by
`opening an issue on GitHub <https://github.com/daq-tools/kotori/issues/new>`_
or reaching out to ``support@getkotori.org``. Thank you very much.
