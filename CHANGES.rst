**************
Kotori CHANGES
**************

develop
=======

vendor :ref:`vendor-lst`
------------------------
- resolve collision on parsed C header files when using identical filenames for different channels
- add project "proptest"

vendor :ref:`vendor-hiveeyes`
-----------------------------
- improve configuration file “hiveeyes.ini” and logging
- fix Grafana panel creation
- fix Grafana panel creation re. InfluxDB select expression
- Grafana 2.6.0 compatibility, Grafana 2.1.3 still works though
- don’t put global realm “hiveeyes” into Grafana dashboard name
- improve Grafana panel automation
- accept single values on mqtt topic
- tune the default Grafana dashboard and panel
- documentation updates

packaging
---------
- Modularize python dependencies into extra features
- Debian packaging using FPM

    - Read designated package version from setup.py
    - Use virtualenv-tools for relocating virtualenvs
    - Add systemd service configuration file

miscellaneous
-------------
- Documentation refactoring and improvements


2015-11-26 0.5.1
================
- overhaul configuration files, activate “hydro2motion” channel with vendor “lst”
- fix hydro2motion re. database authentication
- lst: improve documentation


2015-11-26 0.5.0
================

vendor :ref:`vendor-lst`
------------------------
- add sattracker application
- fix WAMP serialization error when publishing binary data (e.g. "char 0x9c") by using MsgPack serialization
- augment c source file before compilation re. ``#include "mbed.h"`` vs. ``#include "stdint.h"``
- parse transformation rules from source code annotation
- apply transformation rules before publishing to software bus
- fix grafana dashboard update when having no panels
- nasty hack to get proper struct initializer data from CParser results
- show “average” column in Grafana
- flexible compiler detection re. Linux vs. Mac OSX (MacPorts)
- improve error handling when using interactive commands
- explicitly convert values to float when evaluating SymPy expressions
- influxdb: prevent float<->integer casting errors by converting all numerical values to float
- upgrade to python influxdb-2.10.0
- rename ``etc/lst-h2m.ini`` to ``etc/lst.ini``
- generalize h2m-message and sattracker-message into lst-message
- specify configuration file via KOTORI_CONFIG environment variable
- add “lst-message list-channels” command
- wording: change “application” to “channel”
- refactor configuration mechanics


.. _v0.4.0:

2015-11-20 0.4.0
================

proof-of-concept for vendor :ref:`vendor-lst`
---------------------------------------------
- add struct definitions of h2m project
- add basic udp message sender in c++ based on h2m struct definitions
- add infrastructure for parsing schema mappings from c/c++ header files based on pyclibrary
- instantiate structs from compiled c/c++ header files/libraries
- introduce struct registry for bookkeeping and runtime dispatching
- decouple lst/h2m specific struct registry behavior based on ID attribute
- add initial docs about lst/h2m spikes
- properly tweak "h2m_structs.h" to be grokked by patched pyclibrary
- make message receiving actually work in dry-dock, improve pretty-printing
- add command line entrypoint “h2m-message” with “decode” and “info” actions
- implement “h2m-message send”
- lst main application component: receive, decode and store binary messages
- automatic Grafana dashboard- and panel creation

general improvements
--------------------
- add release and documentation infrastructure through Makefile targets
- fix panel generation for vendor hiveeyes
- use nanosecond time precision with InfluxDB
- lst: honour struct field order in Grafana
- add more details to Grafana dashboard panels
- improve error messages “h2m-message send/decode”
- generalize c library adapter, multi-project capabilities for vendor lst


2015-11-06 0.3.2
================

proof-of-concept for vendor :ref:`vendor-hiveeyes`
--------------------------------------------------
- upgrade foundation libraries: Twisted, Autobahn, Crossbar
- receive messages via MQTT and store data points into InfluxDB
- storage: add support for InfluxDB 0.9
- storage: minor tweaks to enable influxdb database authentication
- receive telemetry data from BERadio
- grafana datasource- and dashboard automation
- Sort "collect_fields" result before passing to grafana manager

vendor :ref:`vendor-hydro2motion`
---------------------------------
- refactor hydro2motion code

user interface
--------------
- add frontend foundation based on Pyramid web framework
- add jQuery, Bootstrap, Fontawesome, html5shiv and respond.js
- add material design for bootstrap
- add prototype html based on SB Admin 2 bootstrap template
- add modernizr and underscore
- add foundation for page transitions from codrops
- http: cache really static resources longer than volatile ones
- ui: add pages with page transitions, about content, etc.

general improvements
--------------------
- refactor project layout
- use configuration file instead of hardcoded configuration values
- improve logging


2015-05-21 0.2.2
================
- hydro2motion: production improvements from May 2015 in Rotterdam


2015-05-01 0.2.1
================

vendor :ref:`vendor-hydro2motion`
---------------------------------
- ui: set map position to Munich
- ui: add lat long conversion
- backend: use InfluxDB on localhost
- backend: process complete Fuelcell telemetry data package


2015-04-24 0.2.0
================

proof-of-concept for vendor :ref:`vendor-hydro2motion`
------------------------------------------------------
- ui: add d3 and rickshaw
- ui: add timeseries prototype
- ui: add cbuffer.js
- ui: use ringbuffer for telemetry data
- backend: more convenient default setting: listen on all interfaces
- sensors: add temp sensor
- backend: store telemetry data to sqlite database
- middleware: reduce lag because of debug messages
- middleware: disable heartbeat
- backend: add mongodb adapter
- ui: add leaflet map
- ui: fix image baseurl for leaflet.js
- ui: add marker to leaflet widget
- ui: be graceful to old wire format for telemetry data
- backend: store latitude and longitude into databases
- ui: mapview: let the marker follow the position (map.panTo), but disable it
- backend: add database adapter for InfluxDB and some documentation along the lines
- improve documentation


2015-03-18 0.1.1
================
- ui/backend: add persistent configuration store
- ui: add bootstrap-editable css
- namespace refactoring from ilaundry.node to kotori.node
- upgrade javascript libraries to autobahn 0.10.1, add crossbar configuration
- partial upgrade to autobahn 0.10.1
- backend: add udp adapter


2014-01-21 0.1.0
================
- node: reactivate heartbeat
- node: mplayer user-agent hack for correctly spelling umlauts
- ui: indicate motion activity from node
- ui: indicate node online/offline state
- ui: indicate privacy mode
- ui: button for toggling operator presence
- ether: refactored node registration, send hostname along
- ui: layout refactoring, display more details


2014-01-13 0.0.4
================
- ui: introduce Bootstrap, jQuery, underscore, etc.
- ui: reflect multinode capabilities


2014-01-13 0.0.3
================
- modularized into three components: master, node, web
- single-daemon mode
- first feature set on top of Adafruit_BBIO.GPIO


2014-01-05 0.0.2
================
- Multiple nodes for real [NodeRegistry]


2014-01-05 0.0.1
================

proof-of-concept for vendor :ref:`vendor-ilaundry`
--------------------------------------------------
- Two daemons: master service and node service
- Communication infrastructure on top of Autobahn using PubSub
- Text-to-speech on top of Google Translate TTS
- Basic HTML Dashboard GUI for sending text messages
