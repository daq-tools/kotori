===============
iLaundry README
===============

Get code
--------
::

    git clone git@git.elmyra.de:elbasi/useeds-ilaundry.git
    cd useeds-ilaundry


Setup prerequisites
-------------------
::

    apt-get install python-twisted      # or "pip install Twisted"
    apt-get install python-virtualenv python-dev


Setup node sandbox
------------------
::

    apt-get install mplayer

    virtualenv-2.7 --system-site-packages .venv27
    source .venv27/bin/activate
    pip install distribute==0.6.45
    pip install Adafruit_BBIO

    cd src/ilaundry.node
    python setup.py develop
    cd -


Setup master sandbox
--------------------
::

    virtualenv-2.7 --no-site-packages .venv27
    source .venv27/bin/activate

    cd src/ilaundry.master
    python setup.py develop
    cd -


Run daemons
-----------
single daemon, serve master, node and web gui::

    ilaundry --debug

    # visit web dashboard: http://localhost:35000

master only::

    ilaundry master --debug

node only::

    ilaundry node --master=ws://beaglebone.local:9000 --debug
    ilaundry node --master=ws://master.ilaundry.useeds.elmyra.de:9000 --debug
