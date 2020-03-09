.. include:: ../_resources.rst

.. _firmware-builder:

################
Firmware builder
################


*****
Intro
*****
For vendor :ref:`vendor-hiveeyes`, there's a requirement for automating builds
of Arduino projects using a flexible and powerful build system.
This infrastructure pulls code sketches including dependencies from the
`Hiveeyes Arduino repository`_, replaces user-defined variables in the main
sketch as well as the ``Makefile`` and delivers customized firmwares based
on an universal code base.

The main use case for this is to enable everyone to build her own firmwares
without installing any toolchain at all. The most prominent example for customizing
user-defined variables would be the Hiveeyes WAN device address in form of the triple
(``HE_USER``, ``HE_SITE``, ``HE_HIVE``) or the access point configuration parameters
for setting up a GPRS device for communication in form of the quadruple
(``GPRSBEE_AP_NAME``, ``GPRSBEE_AP_AUTH``, ``GPRSBEE_AP_USER`` and ``GPRSBEE_AP_PASS``).

For getting an idea about the variable replacements with an example sketch suitable for
automatic building using the variables described above, please have a look at
`node-gprs-any.ino, line 81 ff. <https://github.com/hiveeyes/arduino/blob/master/node-gprs-any/node-gprs-any.ino#L81#>`_

See :ref:`hiveeyes-arduino:open-hive-firmware` about how this is used in production.


******
Server
******
Setup prerequisites::

    aptitude install arduino-core

Configure the firmware builder application similar to the Hiveeyes example blueprint:

.. literalinclude:: ../_static/content/etc/examples/firmware.ini
    :language: ini
    :linenos:
    :emphasize-lines: 21-30




*****
Usage
*****
.. highlight:: bash

Just send a HTTP POST request to the ``..../firmware.hex``
endpoint using the HTTP client of your choice. Pass the
user-defined variables in JSON or x-www-form-urlencoded
format in the request body.

Setup HTTP client::

    # Debian-based systems
    aptitude install httpie

    # Mac OSX
    sudo port install httpie

Acquire firmware::

    http --timeout=120 --download POST \
        http://localhost:24642/api/hiveeyes/testdrive/area-42/node-1/firmware.hex \
        ref=master path=node-gprs-any makefile=Makefile-Linux.mk \
        GPRSBEE_AP_NAME=internet.eplus.de GPRSBEE_AP_USER=barney@blau.de GPRSBEE_AP_PASS=123

This should deliver a hex file ready for programming::

    Downloading to "hiveeyes_node-gprs-any_avr-pro328-atmega328p_7b8c6790-GPRSBEE_AP_NAME=internet.eplus.de,GPRSBEE_AP_PASS=123,HE_HIVE=node-1,HE_SITE=area-42,HE_USER=testdrive,GPRSBEE_AP_USER=barney@blau.de.hex"
    Done. 53.57 kB in 0.00064s (81.48 MB/s)

Given, the filename is huge, but it includes each and every parameter
to distinguish different build artifacts from each other.

.. tip::

    - There's also an endpoint with suffix ``firmware.elf`` which can be used to obtain
      a firmware binary in `ELF format <ELF_>`_.
    - When running Kotori on your workstation, you might want to use ``Makefile-OSX.mk``
      as designated Makefile.

.. todo::

    How to program the firmware (e.g. using avrdude)?

    - Windows: http://m8051.blogspot.de/2015/01/avrdude-on-windows-long-time-after.html
    - Mac OS X: https://www.pololu.com/docs/0J36/5.c, https://www.obdev.at/products/crosspack/


*******
Details
*******


Performance
===========
The speed of (re)builds depends mainly on the time required to clone, fetch or update from the remote repository.

Example: It might take about two minutes to clone https://github.com/hiveeyes/arduino including updating all
git submodules. However, when disabling the git submodule update process by using ``update_submodules=false``,
it can come down to a few seconds.

It is totally okay to run with ``update_submodules=false`` when you are
sure the git submodules haven't been updated. This is usually not very often.

