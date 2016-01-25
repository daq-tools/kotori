============
Linux Comedi
============

The Control and Measurement Device Interface.

Intro
=====

The Comedi project develops open-source drivers, tools, and libraries for data acquisition.

Comedi is a collection of drivers for a variety of common data acquisition plug-in boards.
The drivers are implemented as a core Linux kernel module providing common functionality
and individual low-level driver modules.

Comedilib is a user-space library that provides a developer-friendly interface to Comedi
devices. Included in the Comedilib distribution is documentation, configuration and
calibration utilities, and demonstration programs.

Kcomedilib is a Linux kernel module (distributed with Comedi) that provides the same
interface as Comedilib in kernel space, suitable for real-time tasks. It is effectively
a "kernel library" for using Comedi from real-time tasks.

- http://www.comedi.org/
- http://www.linux-usb-daq.co.uk/comedi/pdf/comedilib.pdf
- http://www.comedi.org/doc/lowleveldrivers.html
- https://pypi.python.org/pypi/pycomedi/
- https://github.com/wking/pycomedi
- http://sourceforge.net/projects/schlang/


Handbook
========

Setup
-----

http://www.comedi.org/doc/install.html

::

    uname -a
    Linux lablab 4.2.0-1-amd64 #1 SMP Debian 4.2.3-2 (2015-10-14) x86_64 GNU/Linux

    aptitude install libcomedi0 python-comedilib


/etc/modprobe.d/comedi.conf::

    options comedi comedi_num_legacy_minors=4


if ``l /dev/comedi*`` shows no devices, issue::

    for i in `seq 0 15`; do mknod -m 666 /dev/comedi$i c 98 $i; done;


::
    modprobe comedi_test

dmesg::

    [5527065.958917] comedi: module is from the staging directory, the quality is unknown, you have been warned.
    [5527065.959659] comedi: version 0.7.76 - http://www.comedi.org
    [5527125.524709] comedi_test: module is from the staging directory, the quality is unknown, you have been warned.

::

    lsmod | grep comedi
    comedi_test            16384  0
    comedi                 65536  1 comedi_test


::

    cat /proc/comedi
    comedi version 0.7.76
    format string: "%2d: %-20s %-20s %4d", i, driver_name, board_name, n_subdevices
    no devices
    comedi_test:
     comedi_test



Configure device
................
::

    comedi_config /dev/comedi0 comedi_test

dmesg::

    [5528564.009252] comedi comedi0: comedi_test: 1000000 microvolt, 100000 microsecond waveform attached


::

    cat /proc/comedi
    comedi version 0.7.76
    format string: "%2d: %-20s %-20s %4d", i, driver_name, board_name, n_subdevices
     0: comedi_test          comedi_test             2
    comedi_test:
     comedi_test


Operation
---------

Without access to appropriate hardware, let's use channels from the *comedi_test* device.
http://lxr.free-electrons.com/source/drivers/staging/comedi/drivers/comedi_test.c


comedi_test
...........

... generates fake waveforms

http://www.comedi.org/doc/lowleveldrivers.html#idm140692783667536

Description::

    This driver is mainly for testing purposes, but can also be used to
    generate sample waveforms on systems that don't have data acquisition
    hardware.

    Configuration options:
      [0] - Amplitude in microvolts for fake waveforms (default 1 volt)
      [1] - Period in microseconds for fake waveforms (default 0.1 sec)

    Generates a sawtooth wave on channel 0, square wave on channel 1, additional
    waveforms could be added to other channels (currently they return flatline
    zero volts).



::

    $ comedi_test -t info
    I: Comedi version: 0.7.76
    I: Comedilib version: unknown =)
    I: driver name: comedi_test
    I: device name: comedi_test
    I:
    I: subdevice 0
    I: testing info...
    rev 1
    I: subdevice type: 1 (analog input)
      number of channels: 8
      max data value: 65535
      ranges:
        all chans: [-10,10] [-5,5]
    I:
    I: subdevice 1
    I: testing info...
    rev 1
    I: subdevice type: 2 (analog output)
      number of channels: 8
      max data value: 65535
      ranges:
        all chans: [-10,10] [-5,5]


::

    $ comedi_board_info
    overall info:
      version code: 0x00074c
      driver name: comedi_test
      board name: comedi_test
      number of subdevices: 2
    subdevice 0:
      type: 1 (analog input)
      flags: 0x00119000
      number of channels: 8
      max data value: 65535
      ranges:
        all chans: [-10 V,10 V] [-5 V,5 V]
      command:
        start: now
        scan_begin: timer
        convert: now|timer
        scan_end: count
        stop: none|count
      command structure filled with probe_cmd_generic_timed for 1 channels:
        start: now 0
        scan_begin: timer 1000
        convert: now 0
        scan_end: count 1
        stop: count 2
    subdevice 1:
      type: 2 (analog output)
      flags: 0x00120000
      number of channels: 8
      max data value: 65535
      ranges:
        all chans: [-10 V,10 V] [-5 V,5 V]
      command:
        not supported


Crashes machine::

    $ comedi_test -t read_select
    I: Comedi version: 0.7.76
    I: Comedilib version: unknown =)
    I: driver name: comedi_test
    I: device name: comedi_test
    I:
    I: subdevice 0
    I: testing read_select...

    packet_write_wait: Connection to xx.xx.xx.xx: Broken pipe



Try Python

::

    aptitude install cython python-numpy libcomedi-dev

    virtualenv --system-site-packages .venv27
    source .venv27/bin/activate
    #pip install numpy
    #pip install pycomedi

    # https://github.com/wking/pycomedi
    wget https://github.com/wking/pycomedi/archive/master.zip


