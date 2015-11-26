.. include:: ../_resources.rst

.. _vendor-lst:

############################
LST: Labor für Systemtechnik
############################

.. contents:: Table of Contents
   :local:
   :depth: 3

.. highlight:: bash


=====
Goals
=====
- Receive telemetry messages over UDP in binary format.
- Decode and enrich them by using information from structs of real *C/C++* header files.
- Store measurements to database, with attribute names matching the header file struct declarations.
- While doing all this, it should get out of the way by honoring *LST* best practices:

    - Must handle and dispatch to multiple struct definitions per project. Each struct has a unique ID at the second
      byte position. When receiving binary payloads from UDP, the messages have to be dispatched appropriately. Example::

        # This is a struct mapped to message ID=1 (with length=9)
        struct struct_position
        {
            uint8_t  length             ;//1        // Length of struct (number of bytes)
            uint8_t  ID                 ;//2        // Struct ID
            // ...
        } position = {9,1};

    - Must handle bit fields, e.g.::

        uint8_t  send_ser        : 1;   //  3.0 FlagByte 1
        uint8_t  cfg_loaded      : 1;   //  3.1
        uint8_t  clamped         : 1;   //  3.2


===========
Integration
===========
For making a micro controller send UDP messages the *LST* way, please consider using the fine
`H2M Telemetry library <https://developer.mbed.org/users/HMFK03LST1/code/Telemetrie_eth_h2m/>`_
for mbed_ by Sebastian Donner. This was conceived when working on the Hydro2Motion_ project.



========
Handbook
========

Channel configuration
=====================

Channel configuration is currently done by amending the Kotori configuration file,
which is ``/home/basti/kotori/etc/lst.ini`` on host ``kotori-lst``.

.. highlight:: ini

Overview
--------

A channel is made of ...
    - an UDP port for receiving messages
    - a WAMP topic for publishing received messages to the software bus
    - a filesystem path to the directory of C/C++ header files
    - the names of the header files containing struct declarations describing the messages received on a channel,
      see :ref:`lst-header-file-anatomy`

Example::

    [lst]
    channels     = lst-h2m, lst-sattracker

    [lst-h2m]
    udp_port     = 8888
    wamp_topic   = edu.hm.lst.h2m
    include_path = etc/headers
    header_files = h2m_structs.h

    [lst-sattracker]
    udp_port     = 8889
    wamp_topic   = edu.hm.lst.sattracker
    include_path = etc/headers
    header_files = sattracker.h


Add new channel
---------------
- Choose a project/channel name, here "foo"
- Choose an UDP port, here "8890"
- Choose a wamp topic, here "edu.hm.lst.foo"
- Put your C++ header file into the ``etc/headers`` directory, here "foo.h"
- Activate channel configuration by adding configuration section name to the ``channel`` attribute
  of the toplevel ``[lst]`` section, here "lst-foo". This is a comma-separated list.

Example::

    [lst]
    channels     = lst-h2m, lst-sattracker, lst-foo

    # [...]

    [lst-foo]
    udp_port     = 8890
    wamp_topic   = edu.hm.lst.foo
    include_path = etc/headers
    header_files = foo.h

.. note::

    We are working on the *brace-or-equal-initializer* style as well.


.. _lst-header-file-anatomy:

Anatomy of a header file
------------------------
In order to make Kotori grok the message structs defined in standard C/C++ header files, there are some specific details
to be followed. The initializer flavor to be used currently is the "list-initializer" style as seen below.
Further, transformation rules can be attached to specific fields by adding annotations in comments.
See also example below and :ref:`lst-transformation-rules`.

.. highlight:: c++

Example::

    #include "mbed.h"

    struct struct_system
    {
        uint8_t length              ;//1
        uint8_t ID                  ;//2
        uint8_t output      : 1     ;//3.0
        uint8_t use_gps     : 1     ;//3.1
        uint8_t flagbyte_2          ;//4
        double  lat_home            ;//12
        double  long_home           ;//20
        int8_t  sync                ;//4
        uint8_t ck                  ;//21
    } sys = {21,0};

    struct struct_position
    {
        uint8_t  length             ;//1
        uint8_t  ID                 ;//2
        uint8_t  flagbyte_1         ;//3
        uint8_t  flagbyte_2         ;//4
        int16_t  hdg                ;//6     // @rule: name=heading; expr=hdg * 20.1; unit=degrees
        int16_t  pitch              ;//8     // @rule: name=pitch; expr=pitch * 10; unit=degrees
        uint8_t  ck                 ;//9
    } position = {9,1};


.. highlight:: bash

Please consider adding the header file to the git repository by issuing::

    git add etc/headers/your_header.h
    git commit etc/headers/your_header.h
    git push


.. _lst-transformation-rules:

Transformation rules
--------------------

.. highlight:: c++

The purpose of transformation rules is to apply scaling factors to values and to rename fields.
This is achieved by adding a declarative annotation on the same line of the struct field definition. Example::

    int16_t  hdg                ;//6     // @rule: name=heading; expr=hdg * 20.1; unit=degrees

This will:
    - rename the field from "hdg" to "heading"
    - perform scaling by applying the factor 20.1 to the raw value
    - configure value unit "degrees" in Grafana (TODO)

The evaluation of expressions is based on the fine SymPy_ library and can be made of a number of mathematical
expressions, see also `SymPy Features`_.

There's a commandline tool for applying transformation rules to payloads, see :ref:`lst-message-transform`.


Operating Kotori LST
====================

.. highlight:: bash

There is some tooling for conveniently working with native binary message structs defined in ``etc/headers/*.h``.

The general syntax is::

    lst-message <channel> <action> <argument> --config etc/lst.ini

#. ``<channel>`` is one of ``h2m`` or ``sattracker``, see also ":ref:`lst-list-channels`":

    - ``h2m``: Use structs declared in ``etc/headers/h2m_structs.h``
    - ``sattracker``: Use structs declared in ``etc/headers/sattracker.h``

#. ``<action>`` is one of ``decode``, ``transform``, ``send`` or ``info``:

    - ``decode``: Decode binary payload given as hexadecimal string, dispatch to appropriate message matching the ``ID`` field and pretty print the contents
    - ``transform``: Same as ``decode``, but also applies transformation rules, see :ref:`lst-transformation-rules`
    - ``send``: Send binary payload given as hexadecimal string to specified target
    - ``info``: Displays schema information and metadata for given struct name


.. seealso::
    ::

        $ lst-message --help
            Usage:
              lst-message list-channels                    [--config etc/kotori.ini]
              lst-message <channel>  decode     <payload>  [--config etc/kotori.ini] [--debug]
              lst-message <channel>  transform  <payload>  [--config etc/kotori.ini] [--debug]
              lst-message <channel>  send       <payload>  --target=udp://localhost:8888 [--config etc/kotori.ini]
              lst-message <channel>  info       <name>     [--config etc/kotori.ini] [--debug]
              lst-message --version
              lst-message (-h | --help)

            Options:
              --config etc/kotori.ini   Use specified configuration file, otherwise try KOTORI_CONFIG environment variable
              --version                 Show version information
              --debug                   Enable debug messages
              -h --help                 Show this screen

.. note::

    The parameter ``--config etc/lst.ini`` can be omitted by defining the ``KOTORI_CONFIG`` environment variable::

        export KOTORI_CONFIG=`pwd`/etc/lst.ini


.. _lst-list-channels:

Show list of channels
---------------------
::

    $ lst-message list-channels

    Channel names:
    lst-h2m
    lst-sattracker

So, the canonical channel names are "h2m" and "sattracker".
They can be configured in Kotori configuration file, e.g. ``etc/lst.ini``.
Use them as the ``<channel>`` parameter to ``lst-message`` in the following commands.


Decode message
--------------
Decode a short message in hex format, display struct name and decoded content::

    $ lst-message h2m decode 0x05022a0021
    ----
    name         struct_cap_r
    ----
    hex          0x05022a0021
    decimal      [5, 2, 42, 0, 33]
    bytes        '\x05\x02*\x00!'
    ----
    length       5
    ID           2
    voltage_act  42
    ck           33



.. _lst-message-transform:

Transform message
-----------------
Same as ``decode``, but also applies transformation rules, see :ref:`lst-transformation-rules`.

Example::

    $ lst-message sattracker transform 0x090100000100000000
    ----
    name        struct_position
    ----
    hex         0x090100000100000000
    decimal     [9, 1, 0, 0, 1, 0, 0, 0, 0]
    bytes       '\t\x01\x00\x00\x01\x00\x00\x00\x00'
    ----
    length      9
    ID          1
    flagbyte_1  0
    flagbyte_2  0
    heading     42.42
    pitch       0
    ck          0

The field ``heading`` was augmented by the transformation rule::

    // @rule: name=heading; expr=hdg * 42.42; unit=degrees


Send message
------------
Send a message in hex format to UDP server::

    $ lst-message h2m send 0x05022a0021 --target=udp://localhost:8888
    Message "0x05022a0021" sent to "udp://localhost:8888"

Use this tool to generate and send binary messages without having the hardware in place.


Display message schema
----------------------
Display struct metadata information::

    $ lst-message h2m info struct_fuelcell_r

    ------------------------------------------------------------------------------------
                                 struct "struct_fuelcell_r"
    ------------------------------------------------------------------------------------

    Header information

    name         type        default    bitfield
    -----------  --------  ---------  ----------
    length       uint8_t          11
    ID           uint8_t           4
    current_act  uint16_t
    current_req  uint16_t
    voltage_act  uint16_t
    voltage_req  uint16_t
    ck           uint8_t


    Library information

    name         type      symbol    field                                   bitfield
    -----------  --------  --------  ------------------------------------  ----------
    length       c_ubyte   B         <Field type=c_ubyte, ofs=0, size=1>
    ID           c_ubyte   B         <Field type=c_ubyte, ofs=1, size=1>
    current_act  c_ushort  H         <Field type=c_ushort, ofs=2, size=2>
    current_req  c_ushort  H         <Field type=c_ushort, ofs=4, size=2>
    voltage_act  c_ushort  H         <Field type=c_ushort, ofs=6, size=2>
    voltage_req  c_ushort  H         <Field type=c_ushort, ofs=8, size=2>
    ck           c_ubyte   B         <Field type=c_ubyte, ofs=10, size=1>


    Representations

    kind     representation
    -------  ----------------------------------------------
    hex      0x0b04000000000000000000
    decimal  [11, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    bytes    '\x0b\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00'


Todo
----
::

    $ lst-message h2m encode
    $ lst-message h2m receive


Query InfluxDB
==============

List databases::

    $ curl --silent --get 'http://192.168.59.103:8086/query?pretty=true' --user admin:Armoojwi --data-urlencode 'q=SHOW DATABASES' | jq '.'

    {
      "results": [
        {
          "series": [
            {
              "name": "databases",
              "columns": [
                "name"
              ],
              "values": [
                [
                  "_internal"
                ],
                [
                  "edu_hm_lst_h2m"
                ]
              ]
            }
          ]
        }
      ]
    }

Query timeseries::

    $ export INFLUX_URI=http://192.168.59.103:8086/query?pretty=true
    $ curl --silent --get $INFLUX_URI --user admin:Armoojwi --data-urlencode 'db=edu_hm_lst_h2m' --data-urlencode 'q=select * from "02_cap_r";' | jq '.'

    {
      "results": [
        {
          "series": [
            {
              "name": "02_cap_r",
              "columns": [
                "time",
                "_hex_",
                "voltage_act"
              ],
              "values": [
                [
                  "2015-11-10T13:44:43.945864544Z",
                  "05022a0021",
                  42
                ],
                [
                  "2015-11-10T13:46:35.678928928Z",
                  "05022a0021",
                  42
                ],
                [
                  "2015-11-10T14:48:33.475860964Z",
                  "05022a0021",
                  42
                ]
              ]
            }
          ]
        }
      ]
    }


===========
Development
===========

.. seealso:: :ref:`lst-development`

