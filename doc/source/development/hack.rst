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

We are also working on a Vagrant setup to support developers on
different operating systems. See `hivemonitor-vagrant`_.


******
Basics
******

Prepare system
==============
::

    aptitude install python-virtualenv build-essential python-dev libffi-dev libssl-dev


Get the source code
===================
::

    mkdir -p develop
    git clone git@git.elmyra.de:isarengineering/kotori.git develop/kotori
    cd develop/kotori

    make virtualenv
    source .venv27/bin/activate
    python setup.py develop

.. note::
    Please contact us by email at "hiveeyes-devs ät ideensyndikat.org"
    for repository access until the source code is on GitHub.


Run ad hoc
==========
::

    cd develop/kotori
    source .venv27/bin/activate
    kotori --config etc/development.ini --debug

.. note::

    An alternative way to specify the configuration file::

        # config file path environment variable
        export KOTORI_CONFIG=/etc/kotori/kotori.ini

        # start service
        kotori

.. tip:: Sourcing into the virtualenv is not a must, Kotori also can be called directly::

        ~/develop/kotori/.venv27/bin/kotori --config ~/develop/kotori/etc/development.ini --debug


tmux
====

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


PyCharm
=======
Add Project to PyCharm by using "Open Directory..."

There's a Free Community edition of PyCharm_, you should really give it a try.



********
Advanced
********

Manual installation
===================
Python Eggs can be installed into virtualenvs and into the system, both in editable and non-editable modes.

.. seealso::
    | ``--editable`` option:
    | Install a project in editable mode (i.e. setuptools "develop mode") from a local project path or a VCS url.


Install from Python Egg
-----------------------
Into virtualenv::

    mkdir -p ~/develop/kotori
    virtualenv ~/develop/kotori/.venv27
    ~/develop/kotori/.venv27/bin/pip install kotori[daq] \
        --extra-index-url=https://packages.elmyra.de/isarengineering/python/eggs/ \
        --upgrade

Into system::

    aptitude install python-pip
    pip install kotori[daq] \
        --extra-index-url=https://packages.elmyra.de/isarengineering/python/eggs/ \
        --upgrade


Add ``/etc/kotori/kotori.ini``:

.. literalinclude:: ../_static/content/hiveeyes.ini
    :language: ini


Install from git repository
---------------------------
pip even squeezes the extra feature option into the url::

    pip install --editable git+https://git.repo/some_pkg.git#egg=SomePackage
    pip install --editable git+https://git.repo/some_pkg.git@feature#egg=SomePackage

    -- https://pip.pypa.io/en/stable/reference/pip_install/#examples



Run as service
==============
You really should go with the :ref:`setup-debian` packages first.

When still having the desire to run the application
as system service while being in development mode,
have a look at :ref:`systemd-development-mode`.

We actively use this scenario for integration
scenarios, testing and debugging.
