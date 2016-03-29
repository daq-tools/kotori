.. include:: ../_resources.rst

.. _kotori-hacking:

#################
Hacking on Kotori
#################

.. contents::
   :local:
   :depth: 2

----

*****
Intro
*****

We're happy you reached this point. You mean it. Let's go.

For the auxiliary infrastructure (Mosquitto_, InfluxDB_, Grafana_),
you might want to have a look at the :ref:`docker-infrastructure`.
This relies on boot2docker_ and makes us happy when used on Mac OSX.

When running Linux, you might just want to install the infrastructure
on your local workstation natively like :ref:`setup-debian`.

We are also working on a Vagrant setup to support developers on
different operating systems. See `hivemonitor-vagrant`_.


***************
Getting started
***************

Get the source code
===================
::

    mkdir -p develop
    git clone git@git.elmyra.de:isarengineering/kotori.git develop/kotori
    cd develop/kotori

Setup virtualenv
================
::

    make virtualenv
    source .venv27/bin/activate
    python setup.py develop

    # install extras
    pip install -e .[daq]


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
