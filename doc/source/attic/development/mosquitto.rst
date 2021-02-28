:orphan:

.. _mosquitto-on-osx:

Setup Mosquitto on Mac OSX
==========================
::

    wget http://mosquitto.org/files/source/mosquitto-1.4.8.tar.gz
    tar -xzf mosquitto-1.4.8.tar.gz
    cd mosquitto-1.4.8

    cmake .
    make

    sudo cp client/mosquitto_* /usr/local/bin/
    sudo cp src/mosquitto src/mosquitto_passwd /usr/local/bin/

