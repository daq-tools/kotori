================
Kotori DAQ Tasks
================

LST
===

Prio 1
------
- [o] Establish mechanism to reset Grafana Dashboard creation state, the "GrafanaManager.skip_cache"

Prio 2
------
- [o] Intro to the H2M scenario with pictures, drawing, source code (header file) and nice Grafana graph
- [o] Flexible pretending UDP sender programs for generating and sending message struct payloads
- [o] Waveform publishers
- [o] Generate HTML overview of all message struct schemas using tabulate
- [o] Console based message receiver and decoder
- [o] Properly implement checksumming, honor field ``ck``

Prio 3
------
- [o] Maybe use cffi instead of pyclibrary, see https://cffi.readthedocs.org/en/latest/using.html#working-with-pointers-structures-and-arrays

Done
----
- [x] Rename repository to "kotori"
- [x] Publish docs to https://docs.elmyra.de/isar-engineering/kotori/
- [x] Proper commandline interface for encoding and decoding message structs à la ``beradio``
- [x] Publish docs to http://isarengineering.de/docs/kotori/
- [x] The order of fields provisioned into Grafana panel is wrong due to unordered-dict-republishing on Bus
      Example: "03_cap_w" has "voltage_low, voltage_mid, voltage_load, voltage_max, ..."
               but should be  "voltage_low, voltage_mid, voltage_max, voltage_load, ..."
      Proposal: Either publish something self-contained to the Bus which reflects the very order,
                or add some bookkeeping (a struct->fieldname registry) at the decoding level,
                where order is correct. Reuse this information when creating the Grafana stuff.
      Solution: Send data as list of lists to the WAMP bus.
- [x] kotori.daq.intercom.c should perform the compilation step for getting a msglib.so out of a msglib.h
- [x] decouple main application from self.config['lst-h2m']


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


-----------
Milestone 1
-----------
- dynamic receiver channels
- realtime scope views: embed grafana Graphs or render directly e.g. using Rickshaw.js?
    - http://docs.grafana.org/v2.0/reference/sharing/
    - https://github.com/grafana/grafana/issues/1622
    - https://github.com/ricklupton/livefft

-----------
Milestone 2
-----------
- pdf renderer
- derivation and integration



Improve commandline interface
=============================

"""
#kotori ship <name> move <x> <y> [--speed=<kn>]
#kotori ship shoot <x> <y>
#kotori mine (set|remove) <x> <y> [--moored | --drifting]
"""


Embedded use
============

Setup node sandbox
------------------
::

    apt-get install mplayer

    virtualenv-2.7 --system-site-packages .venv27
    source .venv27/bin/activate
    pip install distribute==0.6.45
    pip install Adafruit_BBIO

    cd src/kotori.node
    python setup.py develop
    cd -


Master/node modes
=================

master only::

    kotori master --debug

node only::

    kotori node --master=ws://offgrid:9000/ws --debug
    kotori node --master=ws://beaglebone.local:9000/ws --debug
    kotori node --master=ws://master.example.com:9000/ws --debug

