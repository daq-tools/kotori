.. _firmware-builder:

################
Firmware builder
################


******
Server
******
Setup prerequisites::

    aptitude install arduino-core



*****
Usage
*****
::

    aptitude install httpie

::

    http --timeout=120 --download POST \
        http://localhost:24642/api/hiveeyes/testdrive/area-42/node-1/firmware.hex \
        ref=master path=node-gprs-any makefile=Makefile-Linux.mk \
        GPRSBEE_AP_NAME=internet.eplus.de GPRSBEE_AP_USER=barney@blau.de GPRSBEE_AP_PASS=123


.. todo::

    How to program the firmware (e.g. using avrdude)?

    - Windows: http://m8051.blogspot.de/2015/01/avrdude-on-windows-long-time-after.html
    - Mac OS X: https://www.pololu.com/docs/0J36/5.c, https://www.obdev.at/products/crosspack/

