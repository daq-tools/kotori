==================
kotori-mqtt README
==================


Basic use
=========

Get code
--------
::

    git clone git@git.elmyra.de:isar-engineering/kotori-daq.git
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
    pip install 'setuptools>=18.3.1'

    cd src/kotori.node/
    python setup.py develop



Start database
--------------
- Run InfluxDB Docker container::

    boot2docker up
    eval "$(boot2docker shellinit)"
    docker start influxdb


Start application
-----------------
single daemon, serve master, node and web gui::

    crossbar start
    kotori --config=development.ini --debug

Visit web dashboards at
    - http://localhost:35000
    - http://localhost:36000


Send telemetry data
-------------------
- Open Browser at http://localhost:35000/
- Run::

    kotori-wamp-client
    kotori-udp-client



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
