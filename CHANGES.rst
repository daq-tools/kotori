==============
Kotori CHANGES
==============

develop
-------
- add release and documentation infrastructure through Makefile targets
- add vendor “lst”
    - add struct definitions of h2m project
    - add c++ udp sender
    - add infrastructure for parsing schema mappings from c/c++ header files based on pyclibrary
    - instantiate structs from compiled c/c++ header files/libraries
    - introduce struct registry
    - decouple lst/h2m specific struct registry behavior
    - add initial docs about lst/h2m experiments
    - properly tweak h2m_structs.h


2015-11-06 0.3.2
----------------
- upgrade foundation libraries: Twisted, Autobahn, Crossbar
- add frontend foundation based on Pyramid web framework
- ui: add jQuery, Bootstrap, Fontawesome, html5shiv and respond.js
- ui: add material design for bootstrap
- ui: add prototype html based on SB Admin 2 bootstrap template
- http: cache really static resources longer than volatile ones
- refactor hydro2motion code
- ui: add modernizr and underscore
- ui: add foundation for page transitions from codrops
- add vendor "hiveeyes"
- hiveeyes: receive messages via MQTT and store data points into InfluxDB
- app: use configuration file instead of hardcoded configuration values
- storage: add support for InfluxDB 0.9
- ui: add pages with page transitions, about content, etc.
- storage: minor tweaks to enable influxdb database authentication
- minor update to BERadio receiving
- integrate grafana datasource- and dashboard automation
- improve logging
- Sort "collect_fields" result before passing to grafana manager
- refactor project layout


2015-05-21 0.2.2
----------------
- hydro2motion: production improvements from May 2015 in Rotterdam


2015-05-01 0.2.1
----------------
- hydro2motion: ui: set map position to Munich
- hydro2motion: ui: add lat long conversion
- hydro2motion: backend: use InfluxDB on localhost
- hydro2motion: backend: process complete Fuelcell telemetry data package


2015-04-24 0.2.0
----------------
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
----------------
- ui/backend: add persistent configuration store
- ui: add bootstrap-editable css
- namespace refactoring from ilaundry.node to kotori.node
- upgrade javascript libraries to autobahn 0.10.1, add crossbar configuration
- partial upgrade to autobahn 0.10.1
- backend: add udp adapter


2014-01-21 0.1.0
----------------
- node: reactivate heartbeat
- node: mplayer user-agent hack for correctly spelling umlauts
- ui: indicate motion activity from node
- ui: indicate node online/offline state
- ui: indicate privacy mode
- ui: button for toggling operator presence
- ether: refactored node registration, send hostname along
- ui: layout refactoring, display more details


2014-01-13 0.0.4
----------------
- ui: introduce Bootstrap, jQuery, underscore, etc.
- ui: reflect multinode capabilities


2014-01-13 0.0.3
----------------
- modularized into three components: master, node, web
- single-daemon mode
- first feature set on top of Adafruit_BBIO.GPIO


2014-01-05 0.0.2
----------------
- Multiple nodes for real [NodeRegistry]


2014-01-05 0.0.1
----------------
proof-of-concept

- Two daemons: master service and node service
- Communication infrastructure on top of Autobahn using PubSub
- Text-to-speech on top of Google Translate TTS
- Basic HTML Dashboard GUI for sending text messages
