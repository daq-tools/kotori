============================
Kotori DAQ application setup
============================


Basic use
=========

Get code
--------
::

    git clone git@git.elmyra.de:isar-engineering/kotori-daq.git
    cd kotori-daq


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


Start application
-----------------
crossbar router::

    crossbar start

main application::

    kotori --config=etc/development.ini --debug

Visit web dashboards at
    - http://localhost:35000
    - http://localhost:36000
