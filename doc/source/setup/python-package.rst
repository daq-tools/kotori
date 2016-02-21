.. include:: ../_resources.rst

.. _setup-python-package:

##############
Python package
##############

.. contents:: Table of Contents
   :local:
   :depth: 2

----

*****
Intro
*****
Setting up Kotori as Python package is suitable for general :ref:`kotori-hacking`
or for installing on platforms where there's no native distribution package available yet.

Kotori can be installed in different variants.

Python Eggs can be installed into virtualenvs and into the system, both in editable and non-editable modes.

.. seealso::
    | ``--editable`` option:
    | Install a project in editable mode (i.e. setuptools "develop mode") from a local project path or a VCS url.


*******
Details
*******

Install using PIP
=================

Prerequisites
-------------
::

    # prepare system
    aptitude install python-pip build-essential python-dev libffi-dev libssl-dev


Install from Python source egg
------------------------------
::

    # install latest Kotori release with feature "daq"
    pip install kotori[daq] --extra-index-url=https://packages.elmyra.de/hiveeyes/python/eggs/ --upgrade

.. tip::

    Installing Kotori with ``pip`` inside a Python *virtualenv* would
    be perfect when playing around. You won't need root permissions
    and the Python libraries of your system distribution will stay
    completely untouched.
    See next section for how to setup a Python *virtulenv* environment.
    See also :ref:`kotori-hacking` for getting hold of the git repository
    when installing from source.


Install from git repository
---------------------------
::

    pip install --editable git+https://git.repo/some_pkg.git#egg=SomePackage
    pip install --editable git+https://git.repo/some_pkg.git@feature#egg=SomePackage

.. seealso:: https://pip.pypa.io/en/stable/reference/pip_install/#examples



.. _setup-python-virtualenv:

Install into virtualenv
=======================

Prepare system
--------------
::

    aptitude install python-virtualenv build-essential python-dev libffi-dev libssl-dev

Setup virtualenv
----------------
::

    make virtualenv
    source .venv27/bin/activate
    python setup.py develop


Install manually
================

Q: What is this? Give me the Egg!

A: Here you are::

    wget https://packages.elmyra.de/hiveeyes/python/eggs/kotori/kotori-0.6.0.tar.gz
    tar -xzf kotori-0.6.0.tar.gz
    cd kotori-0.6.0
    python setup.py install
