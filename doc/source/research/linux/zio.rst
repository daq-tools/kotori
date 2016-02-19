=========
Linux ZIO
=========

ZIO: The Ultimate Linux Kernel I/O Framework

Intro
=====
- `ZIO Homepage <zio-homepage_>`_
- `ZIO Manual <zio-manual_>`_
- `ZIO Paper <zio-paper_>`_
- `ZIO Poster <zio-poster_>`_
- `ZIO Slides <zio-slides_>`_
- `ZIO Repository <zio-repository_>`_


See also
--------
- http://www.ohwr.org/projects/zio/wiki/Requirements
- http://www.ohwr.org/projects/fmc-tdc/wiki

.. _zio-homepage: http://www.ohwr.org/projects/zio
.. _zio-manual: http://www.ohwr.org/attachments/download/1840/zio-manual-130121-v1.0.pdf
.. _zio-paper: http://www.ohwr.org/attachments/download/2514/MOMIB09.PDF
.. _zio-poster: http://www.ohwr.org/attachments/download/2516/zio-poster-mp.pdf
.. _zio-slides: http://www.ohwr.org/attachments/download/2515/MOMIB09_TALK.PDF
.. _zio-repository: http://www.ohwr.org/projects/zio/repository



Handbook
========

Setup
-----
::

    aptitude install linux-headers-amd64
    git clone git://ohwr.org/misc/zio.git
    cd zio
    make

README::

    insmod zio.ko
    insmod drivers/zio-zero.ko

::

    lsmod | grep zio
    zio_zero               24576  0
    zio                    81920  7 zio_zero

dmesg::

    [5431949.898785] zio-core had been loaded
    [5432090.752090] zzero zzero-0000: device loaded


Operation
---------

Without access to appropriate hardware, let's use channels from the *zero* device.

zio-manual:

    The zero device is a software-driven input and output device,
    it is used for demonstration and stress-testing. It behaves
    like ``/dev/zero``, ``/dev/null`` and similar devices,
    but it inputs and outputs ZIO blocks.

README::

    zio-zero has three channel sets. cset 0 has three channels.
    They simulate three analog inputs, 8-bits per sample.

         channel 0: returns zero forever
         channel 1: returns random numbers
         channel 2: returns a sawtooth signal (0 to 255 and back)

    [...]

    To read data you can just cat, or "od -t x1" the data device.
    To get control information meta-information) together with data, you
    can use the "zio-dump" user-space utility, in this directory.


Examples::

    ./tools/zio-dump /dev/zio/zzero-0000-0-2-* | more
    Ctrl: version 1.2, trigger user, dev zzero-0000, cset 0, chan 2
    Ctrl: alarms 0x00 0x00
    Ctrl: seq 11462719, n 16, size 1, bits 8, flags 01000001 (little-endian)
    Ctrl: stamp 1447478540.733762335 (0)
    Data: e0 e1 e2 e3 e4 e5 e6 e7 e8 e9 ea eb ec ed ee ef

    ./tools/zio-cat-file /dev/zio/zzero-0000-0-2-data 10 | od -t x1z
    0000000 c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 ca cb cc cd ce cf  >................<
    0000020 d0 d1 d2 d3 d4 d5 d6 d7 d8 d9 da db dc dd de df  >................<
    0000040 e0 e1 e2 e3 e4 e5 e6 e7 e8 e9 ea eb ec ed ee ef  >................<
    0000060 f0 f1 f2 f3 f4 f5 f6 f7 f8 f9 fa fb fc fd fe ff  >................<
    0000100 00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f  >................<
    0000120 10 11 12 13 14 15 16 17 18 19 1a 1b 1c 1d 1e 1f  >................<
    0000140 20 21 22 23 24 25 26 27 28 29 2a 2b 2c 2d 2e 2f  > !"#$%&'()*+,-./<
    0000160 30 31 32 33 34 35 36 37 38 39 3a 3b 3c 3d 3e 3f  >0123456789:;<=>?<
    0000200 40 41 42 43 44 45 46 47 48 49 4a 4b 4c 4d 4e 4f  >@ABCDEFGHIJKLMNO<
    0000220 50 51 52 53 54 55 56 57 58 59 5a 5b 5c 5d 5e 5f  >PQRSTUVWXYZ[\]^_<

    ./tools/zio-cat-file /dev/zio/zzero-0000-0-2-data 10 | od -A n -t x1
     60 61 62 63 64 65 66 67 68 69 6a 6b 6c 6d 6e 6f
     70 71 72 73 74 75 76 77 78 79 7a 7b 7c 7d 7e 7f
     80 81 82 83 84 85 86 87 88 89 8a 8b 8c 8d 8e 8f
     90 91 92 93 94 95 96 97 98 99 9a 9b 9c 9d 9e 9f
     a0 a1 a2 a3 a4 a5 a6 a7 a8 a9 aa ab ac ad ae af
     b0 b1 b2 b3 b4 b5 b6 b7 b8 b9 ba bb bc bd be bf
     c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 ca cb cc cd ce cf
     d0 d1 d2 d3 d4 d5 d6 d7 d8 d9 da db dc dd de df
     e0 e1 e2 e3 e4 e5 e6 e7 e8 e9 ea eb ec ed ee ef
     f0 f1 f2 f3 f4 f5 f6 f7 f8 f9 fa fb fc fd fe ff


Throughput::

    time ./tools/zio-cat-file /dev/zio/zzero-0000-0-2-data 180000 | od -A n -t x1 | wc -w
    ./tools/zio-cat-file: /dev/zio/zzero-0000-0-2-data: no mmap available
    ./tools/zio-cat-file: trasferred 180000 blocks, 2880000 bytes, 1.033464 secs
    2880000

    real	0m1.062s
    user	0m1.288s
    sys	0m0.660s

    => 2.8 million bytes per second. This is 2.8 MHz, right?


PF_ZIO
======
- http://www.ohwr.org/attachments/download/1687/slides-2012-11-pfzio.pdf

PyZio
=====
- https://github.com/FedericoVaga/PyZio


Authors
=======
- | Alessandro Rubini
  | http://www.ohwr.org/users/135
- | Federico Vaga
  | http://www.ohwr.org/users/592
  | https://github.com/FedericoVaga
  | http://www.federicovaga.com/


News
====
- | ZIO 1.0 release announcement
  | http://www.ohwr.org/news/301

