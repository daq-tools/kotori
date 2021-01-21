.. include:: ../../_resources.rst

.. _running-kotori:

######
Kotori
######

*****
Intro
*****
Kotori can be run in different ways.


************
As a service
************
When installed using a distribution package like outlined within :ref:`setup-debian`,
Kotori is usually run through systemd and can be controlled through the usual commands::

    systemctl {start,stop,restart,status} kotori


*************
Interactively
*************

.. _run-python-virtualenv:

Run from virtualenv
===================
::

    cd develop/kotori
    source .venv/bin/activate
    kotori --config etc/development.ini --debug

.. tip:: Sourcing into the virtualenv is not a must, Kotori also can be called directly::

        ~/develop/kotori/.venv/bin/kotori --config ~/develop/kotori/etc/development.ini --debug


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

    ssh kotori@daq.example.org
    tmux new -s kotori
    source ~/develop/kotori/.venv/bin/activate
    kotori --config ~/develop/kotori/etc/vendor.ini --debug

Attach later::

    ssh kotori@daq.example.org
    tmux att -t kotori
