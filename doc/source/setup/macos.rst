.. include:: ../_resources.rst

.. _setup-macos:

##############
Setup on macOS
##############


*******
Preface
*******

This part of the documentation covers the installation of Kotori and the whole
software stack for telemetry data acquisition, processing and visualization on
a macOS system.

The first step to using any software package is getting it properly installed.
Please read this section carefully.

After successfully installing the software, you might want to follow up with
its configuration at :ref:`getting-started`.


************
Introduction
************

Auxiliary services can be installed and run either natively
on macOS through Homebrew or by using Docker.


******
Native
******

Package-based installation
==========================

Setup packages::

    brew install mosquitto influxdb grafana mongodb/brew/mongodb-community

Run individual services::

    # Invoke Mosquitto MQTT broker
    mosquitto

    # Invoke InfluxDB timeseries database
    influxd

    # Run MongoDB
    mongod --dbpath /usr/local/var/mongodb

    # Invoke Grafana
    grafana-server \
        --config=/usr/local/etc/grafana/grafana.ini \
        --homepath /usr/local/share/grafana \
        --packaging=brew \
        cfg:default.paths.logs=/usr/local/var/log/grafana \
        cfg:default.paths.data=/usr/local/var/lib/grafana \
        cfg:default.paths.plugins=/usr/local/var/lib/grafana/plugins

In order to start those services in the background, please read these
instructions::

    brew info mosquitto influxdb grafana | grep Caveats -A8

Install Kotori::

    brew install python
    pip install --user kotori

Testdrive::

    export PATH="~/Library/Python/3.9/bin:$PATH"
    kotori --version

Manual installation
===================

`CrateDB`_ does not offer packages for macOS yet. In order to install it, select and download
a tarball archive from the `CrateDB for macOS`_ downloads folder, and follow the `CrateDB
tarball setup`_ instructions for extracting the tarball, and for running CrateDB.


******
Docker
******

Please have a look at :ref:`setup-docker` in order to run Mosquitto_, CrateDB_, InfluxDB_,
MongoDB_, Grafana_, and Kotori by using Docker.


.. _CrateDB for macOS: https://cdn.crate.io/downloads/releases/cratedb/x64_mac/
.. _CrateDB tarball setup: https://crate.io/docs/crate/tutorials/en/latest/basic/index.html#ad-hoc-unix-macos
