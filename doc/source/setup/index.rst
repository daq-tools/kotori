.. _kotori-setup:

#####
Setup
#####
Kotori can be installed through a Debian package ¹², from the
Python Package Index (PyPI) or from the Git repository.


.. toctree::
    :caption: Baseline setup
    :maxdepth: 1

    debian
    macosx
    arch-linux
    docker
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
