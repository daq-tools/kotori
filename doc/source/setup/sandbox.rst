.. include:: ../_resources.rst

.. _kotori-hacking:
.. _kotori-sandbox:

#########################
Setup development sandbox
#########################


Introduction
============
We're happy you reached this point. You mean it. Let's go.


Prerequisites
=============
You will need InfluxDB_, Grafana_, Mosquitto_ and optionally MongoDB_.

For installing them on your workstation, you might want to have a
look at the :ref:`setup-docker`.

When running Linux, you might just want to install the infrastructure
on your local workstation natively like :ref:`setup-debian`.


Environment
===========


Get the source code
===================
::

    mkdir -p develop; cd !$
    git clone https://github.com/daq-tools/kotori.git
    cd kotori

Setup virtualenv
================
::

    make virtualenv
    source .venv2/bin/activate
    python setup.py develop

    # Install extra features

    # Data acquisition base
    pip install --process-dependency-links --editable .[daq] --verbose

    # Data acquisition base, with export features
    pip install --process-dependency-links --editable .[daq,export] --verbose

    # Data acquisition with data sink for binary payloads
    pip install --process-dependency-links --editable .[daq_binary] --verbose

    # Data storage for RDBMS databases and MongoDB
    pip install --process-dependency-links --editable .[storage_plus] --verbose



Please follow :ref:`setup-python-virtualenv`.

.. _run-on-pypy:

Run on PyPy
===========
::

    sudo port install pypy
    virtualenv --python=pypy .venvpypy5
    source .venvpypy5/bin/activate
    python setup.py develop
    pip install -e .[daq]


Run ad hoc
==========
Please follow :ref:`running-kotori`.


PyCharm
=======
Add Project to PyCharm by using "Open Directory..."

There's a Free Community edition of PyCharm_, you should really give it a try.



Run as service
==============
When having the desire to run the application
as system service even while being in development mode,
have a look at :ref:`systemd-development-mode`.
We actively use this scenario for integration
scenarios, testing and debugging.

