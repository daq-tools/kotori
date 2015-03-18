==================
kotori-mqtt README
==================


Basic use
=========

Get code
--------
::

    git clone git@git.elmyra.de:ums/kotori-mqtt.git
    cd kotori-mqtt


Setup prerequisites
-------------------
::

    apt-get install python-twisted      # or "pip install Twisted"
    apt-get install python-virtualenv python-dev


Setup node sandbox
------------------
::

    virtualenv-2.7 --system-site-packages .venv27
    source .venv27/bin/activate

    python src/kotori.node/setup.py develop


Run daemons
-----------
single daemon, serve master, node and web gui::

    crossbar start
    kotori --debug

    # visit web dashboard: http://localhost:35000

master only::

    kotori master --debug

node only::

    kotori node --master=ws://offgrid:9000/ws --debug
    kotori node --master=ws://beaglebone.local:9000/ws --debug
    kotori node --master=ws://master.example.com:9000/ws --debug


Embedded use
============

Setup node sandbox
------------------
::

    apt-get install mplayer

    virtualenv-2.7 --system-site-packages .venv27
    source .venv27/bin/activate
    pip install distribute==0.6.45
    pip install Adafruit_BBIO

    cd src/kotori.node
    python setup.py develop
    cd -
