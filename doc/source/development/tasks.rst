.. _kotori-tasks:

############
Kotori Tasks
############

****
2016
****

All
===

2016-01-25
----------
- [x] When sending::

    mosquitto_pub -h swarm.hiveeyes.org -t hiveeyes/testdrive/999/1/message-json -m '{"temperature": 42.84}'

first and afterwards::

    mosquitto_pub -h swarm.hiveeyes.org -t hiveeyes/testdrive/area-42/1/message-json -m '{"temperature": 42.84}'


No new panel gets created::

    2016-01-26T00:25:12+0100 [kotori.daq.graphing.grafana      ] INFO: Creating datasource "hiveeyes_testdrive"
    2016-01-26T00:25:12+0100 [kotori.daq.graphing.grafana      ] INFO: Getting dashboard "hiveeyes_testdrive"
    2016-01-26T00:25:12+0100 [kotori.daq.graphing.grafana      ] INFO: panels_exists_titles: [u'temp @ node=1,gw=999']
    2016-01-26T00:25:12+0100 [kotori.daq.graphing.grafana      ] INFO: panels_new_titles:    ['temp']
    2016-01-26T00:25:12+0100 [kotori.daq.graphing.grafana      ] INFO: No missing panels to add


2016-01-26
----------
- [o] Grafana Manager: Create dashboard row per gateway in same network
- [o] MQTT signals on thresholds
- [o] Add email alerts on tresholds
- [o] When sending whole bunches of measurements, ignore fields having leading underscores for Grafana panel creation
- [o] The order of the Grafana panels (temperature, humidity, weight) works in Grafana 2.1.3, but not in Grafana 2.6.0


2016-01-27 A
------------
- [x] systemd init script
- [o] Send measurements by HTTP POST and UDP, republish to MQTT
- [o] Mechanism / button to reset the "testdrive" database (or any other?).
      This is required when changing scalar types (e.g. str -> float64, etc.)

2016-01-27 B
------------
- [o] Numbers and gauges about message throughput
- [o] systemd init script for crossbar

2016-01-28 A
------------
- [o] Get rid of the [vendor] configuration settings, use instead::

    [kotori]
    vendors = hiveeyes

- [o] Packaging
    - [o] Make Debian package
    - [o] polish Makefile
    - [o] proper version schwummsing
    - [o] Update docs
    - [o] Use RAM disk for building::

        mkdir /mnt/ramdisk
        mount -t tmpfs -o size=512m tmpfs /mnt/ramdisk

        - http://www.jamescoyle.net/how-to/943-create-a-ram-disk-in-linux
        - http://www.jamescoyle.net/knowledge/951-the-difference-between-a-tmpfs-and-ramfs-ram-disk
    - [o] Make Debian ARM package
    - [o] Make OPKG package for OpenWRT
        - https://github.com/openwrt/packages
        - http://www.jumpnowtek.com/yocto/Managing-a-private-opkg-repository.html
        - http://www.jumpnowtek.com/yocto/Using-your-build-workstation-as-a-remote-package-repository.html

- [o] Create table panel?
      http://docs.grafana.org/guides/whats-new-in-v2-6/#table-panel

2016-01-28 B
------------
- [o] Improve error message if MQTT daemon isn't listening - currently::

    2016-01-28T21:52:13+0100 [mqtt.client.factory.MQTTFactory  ] INFO: Starting factory <mqtt.client.factory.MQTTFactory instance at 0x7f5105e157a0>
    2016-01-28T21:52:13+0100 [mqtt.client.factory.MQTTFactory  ] INFO: Stopping factory <mqtt.client.factory.MQTTFactory instance at 0x7f5105e157a0>


2016-01-29
----------
- [o] Switch to PAHO
    - https://pypi.python.org/pypi/paho-mqtt/
    - https://www.eclipse.org/paho/clients/python/
    - https://git.eclipse.org/c/paho/org.eclipse.paho.mqtt.python.git/tree/src/paho/mqtt/client.py


Hiveeyes
========

Milestone 1 - Kotori 0.6.0
--------------------------
- Arbeit an der Dokumentation, siehe commits von gestern
- Vorbereitung des Release 0.6.0 im aktuellen Zustand mit den Doku Updates (die 0.5.1 ist vom 26. November)
- Release eines einigermaßen sauberen bzw. benutzbaren Debian Pakets


Milestone 2 - Kotori 0.7.0
--------------------------
- Reguläres refactoring
- MQTT Topic

    - Implementierung der "Content Type" Signalisierung über pseudo-Dateiendungen wie geplant
      (Inspired by Nick O’Leary and Jan-Piet Mens; Acked by Clemens and Richard)::

            hiveeyes/testdrive/area42/hive3/temperature vs. hiveeyes/testdrive/area42/hive3.json

    - Weitere Diskussion und Implementierung der "Direction" Signalisierung (Inspired by computourist, Pushed by Richard)
      Proposal: ``.../node3/{direction}/{sensor}.foo``

- Generalisierung der BERadioNetworkApplication / HiveeyesApplication vendor Architektur
- Verbesserung der service-in-service Infrastruktur mit nativen Twisted service containern
- Flexiblere Anwendungsfälle ähnlich dem von Hiveeyes ermöglichen: mqtt topic first-level segment "hiveeyes/" (the "realm") per Konfigurationsdatei bestimmen (Wunsch von Dazz)
- Einführung von Softwaretests


Research
--------
Mit ein paar Dingen müssen wir uns noch stärker beschäftigen:

- InfluxDB

    - Wie geht man am besten mit InfluxDB-nativen Tags in unserem Kontext um?
    - Bemerkung: Vielleicht war die Trennung auf Datenbank/Tableebene die falsche
      Strategie bzw. es gibt noch weitere, die orthogonal davon zusätzlich oder alternativ sinnvoll sind.

- Grafana

    - Wie kann man hier die Tags aus InfluxDB am besten verarbeiten und in den Dashboards praktisch nutzen?
    - Wie funktionieren Annotations mit InfluxDB?

- Notifications

    - Ausblick: mqttwarn besser mit Kotori integrieren (via API) und
      als universeller Nachrichtenvermittler auf swarm.hiveeyes.org betreiben.


****
2015
****

LST
===

Prio 1 - Showstoppers
---------------------

Besides making it work in approx. 30 min. on the first hand (cheers!), there are some remaining issues making the wash&go usage
of Kotori somehow inconvenient in day-to-day business. Let's fix them.

- Currently nothing on stack.


Prio 1.5 - Important
--------------------
- [o] improve: lst-message sattracker send 0x090100000000000000 --target=udp://localhost:8889
      take --target from configuration, matching channel "sattracker"
- [o] lst-message sattracker list-structs
- [o] Field-level granularity for GrafanaManager to counter field-renaming by rule-adding problem
      i.e. if field "hdg" is renamed to "heading", this won't get reflected in Grafana automatically
- [o] Honour annotation attribute "unit" when adding Grafana panels
- [o] SymPy annotations should be able to declare virtual fields
- [o] reduce logging


Prio 2
------
- [o] troubleshooting docs

    - sattracker-message decode 0x090200000100000000
      configfile: etc/lst-h2m.ini
      2015-11-24 21:52:09,325 [kotori.vendor.lst.commands] ERROR  : Decoding binary data "0x090200000100000000" to struct failed. Struct with id 2 (0x2) not registered.

    - sattracker-message info struct_position2
      configfile: etc/lst-h2m.ini
      2015-11-24 21:52:58,642 [kotori.vendor.lst.commands] ERROR  : No struct named "struct_position2"

- [o] new message command ``h2m|sattracker-message list`` to show all struct names
- [o] new "influxdb" maintenance command with e.g. "drop database"
- [o] pyclibrary upstreaming: patches and ctor issue::

    Traceback (most recent call last):
      File "kotori/daq/intercom/c.py", line 112, in <module>
        main()
      File "kotori/daq/intercom/c.py", line 72, in main
        p = clib.struct_program() #(abc=9)
      File "/Users/amo/dev/foss/open.nshare.de/kotori-mqtt/.venv27/lib/python2.7/site-packages/pyclibrary-0.1.2-py2.7.egg/pyclibrary/c_library.py", line 230, in __getattr__
        obj = self(k, n)
      File "/Users/amo/dev/foss/open.nshare.de/kotori-mqtt/.venv27/lib/python2.7/site-packages/pyclibrary-0.1.2-py2.7.egg/pyclibrary/c_library.py", line 210, in __call__
        self._objs_[typ][name] = self._make_obj_(typ, name)
      File "/Users/amo/dev/foss/open.nshare.de/kotori-mqtt/.venv27/lib/python2.7/site-packages/pyclibrary-0.1.2-py2.7.egg/pyclibrary/c_library.py", line 277, in _make_obj_
        return self._get_struct('structs', n)
      File "/Users/amo/dev/foss/open.nshare.de/kotori-mqtt/.venv27/lib/python2.7/site-packages/pyclibrary-0.1.2-py2.7.egg/pyclibrary/backends/ctypes.py", line 294, in _get_struct
        (m[0], self._get_type(m[1]), m[2]) for m in defs]
    ValueError: number of bits invalid for bit field

- [o] refactor ``config['_active_']`` mechanics in ``lst/application.py``


Prio 3
------
- [o] sanity checks for struct schema e.g. against declared length
- [o] Topic "measurement tightness" / "sending timestamps"
- [o] Properly implement checksumming, honor field ``ck``
      sum up all bytes: 0 to n-1 (w/o ck), then mod 255
- [o] database export
- [o] check with pyclibrary development branch: https://github.com/MatthieuDartiailh/pyclibrary/tree/new-backend-api
- [o] Intro to the H2M scenario with pictures, drawing, source code (header file) and nice Grafana graph
- [o] Flexible pretending UDP sender programs for generating and sending message struct payloads
- [o] Waveform publishers
- [o] Bring xyz-message info|decode|list to the web
- [o] Bring "Add Project" (c header file) to the web, including compilation error messages
- [o] refactor classmethods of LibraryAdapter into separate LibraryAdapterFactory
- [o] cache compilation step
- [o] add link to Telemetry.cpp
- [o] ctor syntax
- [o] make issue @ pyclibrary re. brace-or-equal-initializers:

    http://stackoverflow.com/questions/16782103/initializing-default-values-in-a-struct/16783513#16783513

- [o] highlevel influxdb client
- [o] runtime-update of c struct or restart automatism
    - [o] Make brace-or-equal-initializers work properly.

          ::

              # brace-initializer
              struct_position()
              : length(9), ID(1)
              {}

          ::

              # equal-initializer
              uint8_t  length = 9         ;//1
              uint8_t  ID     = 1         ;//2

      Unfortunately, pyclibrary croaks on the first variant.

      On the other hand, the Mbed compiler croaks on the second variant or the program
      fails to initialize the struct properly at runtime. Let's investigate.

      #. => Make an issue @ upstream re. ctor syntax with small canonical example.
      #. => Investigate why the Mbed compiler doesn't grok the equal-initializer style.

    - [o] Make infrastructure based on typedefs instead of structs to honor initializer semantics
- [o] improve error handling (show full stacktrace in log or web frontend), especially when sending payloads to wrong handlers, e.g.::

        2015-11-26T11:30:12+0100 [kotori.daq.intercom.udp          ] INFO: Received via UDP from 141.39.249.176:61473: 0x303b303b32332e37353b35312e3033323b2d302e303136
        2015-11-26T11:30:12+0100 [kotori.daq.intercom.c            ] ERROR: Struct with id 59 (0x3b) not registered.
        2015-11-26T11:30:12+0100 [twisted.internet.defer           ] CRITICAL: Unhandled error in Deferred:



Prio 4
------
- [o] Generate HTML overview of all message struct schemas using tabulate
- [o] Console based message receiver and decoder
- [o] Establish mechanism to reset Grafana Dashboard creation state, the "GrafanaManager.skip_cache"
- [o] receive messages containing sequential numbers, check database for continuity to determine if data points get lost
- [o] think about automatically updating structs at runtime, e.g. from https://developer.mbed.org/users/HMFK03LST1/code/H2M_2014_race/file/adf68d4b873f/components.cpp
- [o] more header files from LST:
    - https://developer.mbed.org/users/HMFK03LST1/code/H2M_2014_race/file/adf68d4b873f/components.cpp
- [o] investigate cffi
    cffi:
    cffi.api.CDefError: cannot parse "struct_position(): length(9), ID(1) {}"


Done
----
- [x] Rename repository to "kotori"
- [x] Publish docs to https://docs.elmyra.de/isar-engineering/kotori/
- [x] Proper commandline interface for encoding and decoding message structs à la ``beradio``
- [x] Publish docs to http://isarengineering.de/docs/kotori/
- [x] The order of fields provisioned into Grafana panel is wrong due to unordered-dict-republishing on Bus
      - Example: "03_cap_w" has "voltage_low, voltage_mid, voltage_load, voltage_max, ..."
                 but should be  "voltage_low, voltage_mid, voltage_max, voltage_load, ..."
      - Proposal: Either publish something self-contained to the Bus which reflects the very order,
                  or add some bookkeeping (a struct->fieldname registry) at the decoding level,
                  where order is correct. Reuse this information when creating the Grafana stuff.
      - Solution: Send data as list of lists to the WAMP bus.
- [x] kotori.daq.intercom.c should perform the compilation step for getting a msglib.so out of a msglib.h
- [x] decouple main application from self.config['lst-h2m']
- [x] unsanitized log output exception::

    2015-11-20T16:56:57+0100 [kotori.daq.storage.influx        ] INFO: Storage location:  {'series': '01_position', 'database': u'edu_hm_lst_sattracker'}
    2015-11-20T16:56:57+0100 [kotori.daq.storage.influx        ] ERROR: InfluxDBClientError: 401: {"error":"user not found"}
    2015-11-20T16:56:57+0100 [kotori.daq.storage.influx        ] ERROR: Unable to format event {'log_namespace': 'kotori.daq.storage.influx', 'log_level': <LogLevel=error>, 'log_logger': <Logger 'kotori.daq.storage.influx'>, 'log_time': 1448035017.722721, 'log_source': None, 'log_format': 'Processing Bus message failed: 401: {"error":"user not found"}\nERROR: InfluxDBClientError: 401: {{"error":"user not found"}}\n\n------------------------------------------------------------\nEntry point:\nFilename:    /home/basti/kotori/kotori/daq/storage/influx.py\nLine number: 171\nFunction:    bus_receive\nCode:        return self.process_message(self.topic, payload)\n------------------------------------------------------------\nSource of exception:\nFilename:    /home/basti/kotori/.venv27/local/lib/python2.7/site-packages/influxdb-2.9.2-py2.7.egg/influxdb/client.py\nLine number: 247\nFunction:    request\nCode:        raise InfluxDBClientError(response.content, response.status_code)\n\nTraceback (most recent call last):\n  File "/home/basti/kotori/kotori/daq/storage/influx.py", line 171, in bus_receive\n    return self.process_message(self.topic, payload)\n  File "/home/basti/kotori/kotori/daq/storage/influx.py", line 195, in process_message\n    self.store_mes

- [x] non-ascii "char" value can't be published to WAMP Bus

    send message::

        sattracker-message send 0x09010000fe0621019c --target=udp://localhost:8889

    exception::

        2015-11-20T17:32:29+0100 [kotori.daq.intercom.udp          ] INFO: Received via UDP from 192.168.0.40:49153: '\t\x01\x00\x00@\x06H\x01\xf2'
        2015-11-20T17:32:29+0100 [kotori.daq.intercom.udp          ] INFO: Publishing to topic 'edu.hm.lst.sattracker' with realm 'lst': [(u'length', 9), (u'ID', 1), (u'flag_1', 0), (u'hdg', 1600), (u'pitch', 328), (u'ck', '\xf2'), ('_name_', u'struct_position'), ('_hex_', '0901000040064801f2')]
        2015-11-20T17:32:29+0100 [twisted.internet.defer           ] CRITICAL: Unhandled error in Deferred:

        Traceback (most recent call last):
          [...]
          File "/home/basti/kotori/kotori/daq/intercom/udp.py", line 32, in datagramReceived
            yield self.bus.publish(self.topic, data_out)
          File "/home/basti/kotori/.venv27/local/lib/python2.7/site-packages/autobahn-0.10.9-py2.7.egg/autobahn/wamp/protocol.py", line 1034, in publish
            raise e
        autobahn.wamp.exception.SerializationError: WAMP serialization error ('ascii' codec can't decode byte 0xf2 in position 1: ordinal not in range(128))

- [x] Make compiler configurable (/usr/bin/g++ on Linux vs. /opt/local/bin/g++-mp-5 on OSX)

- [x] Field type conflicts in InfluxDB, e.g. when adding a transformation rule on the same name, this changing the data type on an existing field::

        2015-11-22T17:00:52+0100 [kotori.daq.storage.influx        ] ERROR: Processing Bus message failed: 400: write failed: field type conflict: input field "pitch" on measurement "01_position" is type float64, already exists as type integer

            ERROR: InfluxDBClientError: 400: write failed: field type conflict: input field "pitch" on measurement "01_position" is type float64, already exists as type integer

      Here, "pitch" was initially coming in as an Integer, but now has changed its type to a Float64,
      due to applying a transformation rule, which (always) yields floats.

      | => Is it possible (and appropriate) to ALTER TABLE on demand?
      | => At least add possibility to drop database via Web.

      - [x] Upgrade to python module "influxdb-2.10.0" => didn't help
      - [x] Store all numerical data as floats

- [x] C Header parsing convenience

    - [x] Automatically add ``#include "stdint.h"`` (required for types ``uint8_t``, etc.) and
          remove ``#include "mbed.h"`` (croaks on Intel)
    - [x] Improve transcoding convenience by using annotations like
          ``// name=heading; expr=hdg * 20; unit=degrees``, see :ref:`math-expressions`.
          Use it for renaming fields and scaling values in Kotori and assigning units in Grafana.
          => Implemented based on SymPy, use it for flexible scaling.

- [x] proper error message when decoding unknown message
- [x] rename ``lst-h2m.ini`` to ``lst.ini``
- [x] generalize ``h2m-message`` vs. ``sattracker-message`` into ``lst-message``,
      maybe read default config via ``~/.kotori.ini`` which transitively points to ``./etc/lst.ini`` to keep the comfort.
      otherwise, the ini file must be specified every time. Other variant:
      ``export KOTORI_CONFIG=/etc/kotori/lst.ini``
- [x] document how to add a new channel
- [x] document rule-based Transformations
    - syntax
    - math expressions
    - sattracker-message transform
- [x] add to docs: https://developer.mbed.org/users/HMFK03LST1/code/Telemetrie_eth_h2m/


Hiveeyes
========

Prio 1
------
- [x] Fix dashboard creation
- [o] Don't always do CREATE DATABASE hiveeyes_3733a169_70d2_450b_b717_6f002a13716b
      see: root@elbanco:~# tail -f /var/log/influxdb/influxd.log
- [o] Receive timestamp from MQTT and use this one
    - InfluxDB sends "2015-11-14T16:29:42.157025953Z" when accessed via HTTP
    - Timestamps must be in Unix time and are assumed to be in nanoseconds,
      see https://influxdb.com/docs/v0.9/write_protocols/write_syntax.html
- [o] Use UDP for sending measurement points to InfluxDB:
      cli = InfluxDBClient.from_DSN('udp+influxdb://username:pass@localhost:8086/databasename', timeout=5, udp_port=159)


Prio 2
------
- [o] Improve inline docs
- [o] License and open sourcing
- [o] Enhance mechanism of how GrafanaManager (re)creates dashboard, when deleted by user at runtime.
      Currently, dashboards are only created on packages arriving after a Kotori restart.
      They are never ever deleted automatically right now.

Done
----
- [x] Sort "collect_fields" result before passing to grafana manager
- [x] investigate and improve mqtt connection robustness and recycling::

    - MQTTFactory shuts down after exception when storing via InfluxDB::

              File "/home/kotori/develop/kotori-daq/src/kotori.node/kotori/daq/storage/influx.py", line 101, in write_real
                response = self.influx.write_points([self.v08_to_09(chunk)])
              File "/home/kotori/develop/kotori-daq/.venv27/local/lib/python2.7/site-packages/influxdb-2.9.2-py2.7.egg/influxdb/client.py", line 387, in write_points
                tags=tags)
              File "/home/kotori/develop/kotori-daq/.venv27/local/lib/python2.7/site-packages/influxdb-2.9.2-py2.7.egg/influxdb/client.py", line 432, in _write_points
                expected_response_code=204
              File "/home/kotori/develop/kotori-daq/.venv27/local/lib/python2.7/site-packages/influxdb-2.9.2-py2.7.egg/influxdb/client.py", line 277, in write
                headers=headers
              File "/home/kotori/develop/kotori-daq/.venv27/local/lib/python2.7/site-packages/influxdb-2.9.2-py2.7.egg/influxdb/client.py", line 247, in request
                raise InfluxDBClientError(response.content, response.status_code)
            influxdb.exceptions.InfluxDBClientError: 400: unable to parse 'w.t ': invalid field format

        2015-10-20 06:12:59+0200 [-] Stopping factory <mqtt.client.factory.MQTTFactory instance at 0x7fda346ccb48>


General
=======

Prio 1
------
- [x] node registration: send hostname along
- [o] node_id-to-label translator with server-side persistence at master node
- [o] run as init.d daemon

Prio 2
------
- [o] show embedded video when node signals activity
- [o] Bug when speaking umlauts, like "Bolognesääää!"::

    2014-01-13 20:01:24+0100 [MasterServerProtocol,5,77.186.145.150] Traceback (most recent call last):
    2014-01-13 20:01:24+0100 [MasterServerProtocol,5,77.186.145.150]   File ".venv27/local/lib/python2.7/site-packages/autobahn-0.7.0-py2.7.egg/autobahn/wamp.py", line 863, in onMessage
    2014-01-13 20:01:24+0100 [MasterServerProtocol,5,77.186.145.150]     self.factory.dispatch(topicUri, event, exclude, eligible)
    2014-01-13 20:01:24+0100 [MasterServerProtocol,5,77.186.145.150]   File ".venv27/local/lib/python2.7/site-packages/autobahn-0.7.0-py2.7.egg/autobahn/wamp.py", line 1033, in dispatch
    2014-01-13 20:01:24+0100 [MasterServerProtocol,5,77.186.145.150]     log.msg("publish event %s for topicUri %s" % (str(event), topicUri))
    2014-01-13 20:01:24+0100 [MasterServerProtocol,5,77.186.145.150] UnicodeEncodeError: 'ascii' codec can't encode characters in position 8-12: ordinal not in range(128)

Prio 3
------
- [o] send dates in messages
- [o] notifications: Pushover- and SMS-integration
- [o] check realtime things
    - scope
    - livefft: https://github.com/ricklupton/livefft


Milestones
==========

Milestone 1
-----------
- dynamic receiver channels
- realtime scope views: embed grafana Graphs or render directly e.g. using Rickshaw.js?
    - http://docs.grafana.org/v2.0/reference/sharing/
    - https://github.com/grafana/grafana/issues/1622
    - https://github.com/ricklupton/livefft

Milestone 2
-----------
- pdf renderer
- derivation and integration
