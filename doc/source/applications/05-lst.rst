============================
LST: Labor für Systemtechnik
============================

.. contents:: Table of Contents
   :local:
   :depth: 2


Goals
=====
- Receive telemetry messages over UDP in binary format.
- Decode and enrich them by using information from structs of real *C/C++* header files.
- Store measurements to database, with attribute names matching the header file struct declarations.
- While doing all this, it should get out of the way by honoring *LST* best practices:

    - Must handle and dispatch to multiple struct definitions per project, e.g.::

        // each struct has a unique "ID" value at the second byte position
        uint8_t  length = 16;           //  1 Length of struct (byte)
        uint8_t  ID     = 42;           //  2 Struct ID

    - Must handle bit fields, e.g.::

        uint8_t  send_ser        : 1;   //  3.0 FlagByte 1
        uint8_t  cfg_loaded      : 1;   //  3.1
        uint8_t  clamped         : 1;   //  3.2


Handbook
========

There is some tooling for conveniently working with native binary message structs defined in ``h2m_structs.h``.

Decode message
--------------
Decode a short message in hex format, display struct name and decoded content::

    $ h2m-message decode 0x05022a0021
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


Send message
------------
Send a message in hex format to UDP server::

    $ h2m-message send 0x05022a0021 --target=udp://localhost:8888
    Message "0x05022a0021" sent to "udp://localhost:8888"

Use this tool to generate and send binary messages without having the hardware in place.


Display message schema
----------------------
Display struct metadata information::

    $ h2m-message info struct_fuelcell_r

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

    h2m-message encode
    h2m-message receive


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

Development
===========

.. seealso:: :ref:`lst-development`.

