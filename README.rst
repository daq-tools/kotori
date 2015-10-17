==================
kotori-mqtt README
==================


Basic use
=========

Get code
--------
::

    git clone git@git.elmyra.de:isar-engineering/kotori-daq.git
    cd kotori-daq


Setup prerequisites
-------------------
Debian::

    aptitude install python-virtualenv build-essential python-dev libffi-dev libssl-dev

Workstation::

    pip install Twisted


Setup node sandbox
------------------
::

    virtualenv --no-site-packages .venv27
    source .venv27/bin/activate
    pip install 'setuptools>=18.3.1'

    cd src/kotori.node/
    python setup.py develop


Troubleshooting
---------------
problem::

    ImportError: /tmp/easy_install-Scu8_1/cryptography-1.0.2/.eggs/cffi-1.2.1-py2.7-linux-x86_64.egg/_cffi_backend.so: failed to map segment from shared object: Operation not permitted

solution::

    TMPDIR=/var/tmp python setup.py develop


problem::

    pkg_resources.DistributionNotFound: The 'pyasn1' distribution was not found and is required by service-identity

solution::

    pip install pyasn1


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
