.. include:: ../_resources.rst

.. _kotori-hacking:
.. _kotori-sandbox:

#########################
Setup development sandbox
#########################


************
Introduction
************

We are happy you reached this point of the documentation. This will probably
mean you want to setup a development sandbox in order to hack on the source
code. We appreciate that, you mean it. Let's go.


*************
Prerequisites
*************

Environment
===========

Install some needed packages::

    apt-get install python3-venv python3-dev docker-compose mosquitto-clients

Foundation services
===================

You will need InfluxDB_, Grafana_, Mosquitto_ and optionally MongoDB_.

For installing them on your workstation, you might want to have a look at the
:ref:`setup-docker`. When running Linux, you can also install the
infrastructure on your local workstation natively like :ref:`setup-debian`.

The most easy way is to run Mosquitto, InfluxDB, MongoDB and Grafana as Docker
containers::

    make start-foundation-services


***********
Walkthrough
***********

Get the source code
===================
::

    mkdir -p develop; cd !$
    git clone https://github.com/daq-tools/kotori.git
    cd kotori


Setup virtualenv
================
::

    # Create and activate virtualenv
    make setup-virtualenv
    source .venv/bin/activate

    # Set option to make the pip installer prefer binary dependencies
    # This might prevent compilation steps for some of them
    export PIP_PREFER_BINARY=1

    # Install package with all extra features.
    pip install -r requirements-full.txt

    # Install specific extra features.

    # Data acquisition base
    pip install --editable=.[daq]

    # Data acquisition base, with export features
    pip install --editable=.[daq,export]

    # Data acquisition with data sink for binary payloads
    pip install --editable=.[daq_binary]

    # Data storage for RDBMS databases and MongoDB
    pip install --editable=.[storage_plus]


.. note::

    See also :ref:`setup-python-package`.




Run ad hoc
==========
Please follow :ref:`running-kotori`.


PyCharm
=======
Add Project to PyCharm by using "Open Directory..."

There's a Free Community edition of PyCharm_, you should really give it a try.



Run as service
==============
When having the need to run the application as a system service even while
still being in development mode, have a look at :ref:`systemd-development-mode`.
We actively use this scenario for integration scenarios, testing and debugging.
