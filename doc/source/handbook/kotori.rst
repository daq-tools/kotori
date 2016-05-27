.. include:: ../_resources.rst

.. _kotori-handbook:

.. _running-kotori:

##############
Running Kotori
##############

.. contents:: Table of Contents
   :local:
   :depth: 1

----

.. todo::

    - Swap content from here with "setup/kotori.rst"
    - Add content from "Getting started" section of :ref:`Hiveeyes Handbook <hiveeyes:handbook>`

*****
Intro
*****
Kotori can be run in different ways.


*************
Configuration
*************

The configuration file is either ``/etc/kotori/kotori.ini``
or at any other location you want to put the configuration at.
A blueprint is:

.. literalinclude:: ../_static/content/kotori.ini
    :language: ini

.. todo:: Add blueprint for application :ref:`application-mqttkit`.

A blueprint for vendor :ref:`vendor-lst` is:

.. literalinclude:: ../_static/content/vendor-lst.ini
    :language: ini


*******
Running
*******

.. _run-python-virtualenv:

Run from virtualenv
===================
::

    cd develop/kotori
    source .venv27/bin/activate
    kotori --config etc/development.ini --debug

.. tip:: Sourcing into the virtualenv is not a must, Kotori also can be called directly::

        ~/develop/kotori/.venv27/bin/kotori --config ~/develop/kotori/etc/development.ini --debug


.. _run-configuration-file:

Specify the configuration file
==============================
There's an alternative way to specify the configuration file::

    # config file path environment variable
    export KOTORI_CONFIG=/etc/kotori/kotori.ini

    # start service
    kotori


Run inside tmux
===============
tmux can keep your terminal sessions open. You can detach and log out of the server.
Wenn getting back to the keyboard, just log in and reattach to the named terminal::

    aptitude install tmux

Run Kotori in tmux session::

    ssh kotori@elbanco.hiveeyes.org
    tmux new -s kotori
    source ~/develop/kotori/.venv27/bin/activate
    kotori --config ~/develop/kotori/etc/hiveeyes.ini --debug

Attach later::

    ssh kotori@elbanco.hiveeyes.org
    tmux att -t kotori

