============================
LST: Labor für Systemtechnik
============================

Goal:
- Receive binary messages over UDP.
- Decode and enrich them by using information from structs of real C/C++ header files.
- Store measurements to database.


Troubleshooting
===============
::

    TypeError: bit fields not allowed for type c_char

Bit fields must be encoded with integers::

    uint8_t  send_ser        :1; //w 3.0 FlagByte 1
    uint8_t  cfg_loaded      :1; //w 3.1
    uint8_t  clamped         :1; //w 3.2
    uint8_t  gps_input       :1; //w 3.3
    uint8_t  check_input     :1; //w 3.4
    uint8_t  gps_akt         :1; //w 3.5
    uint8_t  base_clock      :1; //w 3.6
    uint8_t  do_O2_IN        :1; //w 3.7

The error would be raised when having::

    char     send_ser        :1; //w 3.0 FlagByte 1
    char     cfg_loaded      :1; //w 3.1
    char     clamped         :1; //w 3.2
    // [...]



UDP sending and receiving
=========================

The simple UDP sender program is currently configured to send UDP messages to ``localhost:8888``::

    udp_client_server::udp_client client("localhost", 8888);


Build ``udp_sender.cpp`` and send some binary messages::

    amo offgrid $ cd ~/dev/foss/open.nshare.de/kotori-daq/kotori/vendor/lst/client/cpp

    $ make run
    ---
    name:   program
    id:     0
    length: 13
      0000  0d 00 03 00 41 01 00 00 00 00 00 00 00           ....A........
    ---
    name:   request
    id:     1
    length: 9
      0000  09 01 21 00 00 00 00 00 00 00 00                 ..!........
    ---
    name:   cap_r
    id:     2
    length: 5
      0000  05 02 28 00 00                                   ..(..
    ---
    name:   cap_w
    id:     3
    length: 15
      0000  0f 03 0a 00 00 00 00 00 00 00 00 00 00 00 00     ...............
    ---
    name:   fuelcell_r
    id:     4
    length: 11
      0000  0b 04 03 00 00 00 00 00 00 00 00                 ...........
    ---
    name:   fuelcell_w
    id:     5
    length: 19
      0000  13 05 50 00 78 00 00 00 00 00 00 00 00 00 00 00  ..P.x...........
      0010  00 00 00                                         ...
    ---
    name:   gps_w
    id:     19
    length: 63
      0000  3f 13 b5 62 01 06 34 00 00 00 00 00 00 00 00 00  ?..b..4.........
      0010  00 00 00 00 63 00 00 00 65 00 00 00 00 00 00 00  ....c...e.......
      0020  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
      0030  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00     ...............


Receive binary messages and dump them hexlified::

    $ socat -x udp-listen:8888 stdout
    > 2015/11/07 18:44:49.945555  length=14 from=0 to=13
     0d 00 03 00 41 01 00 00 00 00 00 00 00 00
    A> 2015/11/07 18:44:49.945715  length=12 from=14 to=25
     09 01 21 00 00 00 00 00 00 00 00 00
        !> 2015/11/07 18:44:49.945746  length=6 from=26 to=31
     05 02 28 00 00 00
    (> 2015/11/07 18:44:49.945766  length=16 from=32 to=47
     0f 03 0a 00 00 00 00 00 00 00 00 00 00 00 00 00

    > 2015/11/07 18:44:49.945828  length=12 from=48 to=59
     0b 04 03 00 00 00 00 00 00 00 00 00

    > 2015/11/07 18:44:49.945869  length=20 from=60 to=79
     13 05 50 00 78 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
    Px> 2015/11/07 18:44:49.945914  length=64 from=80 to=143
     3f 13 b5 62 01 06 34 00 00 00 00 00 00 00 00 00 00 00 00 00 63 00 00 00 65 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00

    < 2015/11/07 18:45:49.202989  length=1 from=0 to=0
     0a


Dry-dock: Use things from "``h2m_structs.h``" headers
=====================================================

Build a library from the ``h2m_structs.h`` headers::

    amo offgrid $ cd ~/dev/foss/open.nshare.de/kotori-daq/kotori/vendor/lst/client/cpp
    $ make lib


Run some simple examples::

    (.venv27)amo offgrid $ cd ~/dev/foss/open.nshare.de/kotori-daq
    $ python kotori/vendor/lst/h2m/message.py


    # create a "cap_r" struct and print attributes with default values
    ------------------------------------------
    sr.create('struct_cap_r')

    thing:  <ctypes struct 'struct_cap_r'>
    length: 5
    ID:     2


    # create a "cap_r" struct overriding default values and print the relevant attributes
    ------------------------------------------
    sr.create('struct_cap_r', ID=88)

    thing:  <ctypes struct 'struct_cap_r'>
    length: 5
    ID:     88


    # get lowlevel pyclibrary ctypes backend handle of "struct_program"
    ------------------------------------------
    struct_program = sr.get('struct_program')

    struct_program (schema):
    <__main__.StructAdapter object at 0x106e37d90>
    thing:       <class 'kotori.daq.intercom.pyclibrary_ext.backend_ctypes.s'>
    length:      <Field type=c_ubyte, ofs=0, size=1>
    ID:          <Field type=c_ubyte, ofs=1, size=1>
    send_ser:    <Field type=c_ubyte, ofs=2:0, bits=1>
    cfg_loaded:  <Field type=c_ubyte, ofs=2:1, bits=1>
    ------------------------------------------
    struct_program (instance):
    thing:       <ctypes struct 'struct_program'>
    length:      13
    ID:          0


    # get lowlevel pyclibrary ctypes backend handle of "struct_cap_r"
    ------------------------------------------
    thing:  <class 'kotori.daq.intercom.pyclibrary_ext.backend_ctypes.s'>
    length: <Field type=c_ubyte, ofs=0, size=1>
    ID:     <Field type=c_ubyte, ofs=1, size=1>
    FIELDS:
    [(u'length', <class 'ctypes.c_ubyte'>),
     (u'ID', <class 'ctypes.c_ubyte'>),
     (u'voltage_act', <class 'ctypes.c_ushort'>),
     (u'ck', <class 'ctypes.c_ubyte'>)]
    DEFAULTS:
    {u'ID': 2, u'length': 5}

