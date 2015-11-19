==================
Kotori application
==================

.. highlight:: bash

Basic use
=========

Get code
--------
::

    git clone git@git.elmyra.de:isarengineering/kotori.git
    cd kotori


Setup python environment
------------------------
::

    virtualenv --no-site-packages .venv27
    source .venv27/bin/activate
    pip install 'setuptools>=18.3.1'    # maybe


Install application in development mode
---------------------------------------
::

    python setup.py develop


Start application
-----------------
Crossbar router::

    crossbar start

Main application::

    kotori --config=etc/development.ini --debug

Visit web dashboards at
    - http://localhost:35000
    - http://localhost:36000


Send some testing data
----------------------
::

    # Send fixed data once
    h2m-csv-udp-client "24000;15718;75813;1756;15253;229;220;204;811;1769;0;0;0;0;0;1;0;12;0;0;0;-18;0;4011;417633984;85402624;472851424;0;12242;43;42;0;0"

    # Continuously send random data
    watch -n0.5 h2m-csv-udp-fuzzer


Troubleshooting
---------------
Problem::

    ImportError: /tmp/easy_install-Scu8_1/cryptography-1.0.2/.eggs/cffi-1.2.1-py2.7-linux-x86_64.egg/_cffi_backend.so: failed to map segment from shared object: Operation not permitted

Solution::

    TMPDIR=/var/tmp python setup.py develop

