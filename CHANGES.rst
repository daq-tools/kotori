*********
Changelog
*********


in progress
===========


.. _kotori-0.11.1:

2017-02-01 0.11.1
=================
- Data export: Fix addressing with relative timestamp, e.g. /data.txt?from=now-30d
  as well as proper handling of ``include`` and ``exclude`` url parameters


.. _kotori-0.11.0:

2017-01-31 0.11.0
=================
- Get rid of ``/bus/mqtt`` in URI for HTTP API
- Delegate MQTT message processing to separate thread
- Run ``CREATE DATABASE`` only once to improve performance
- Accept timestamp field ``time`` from sensor readings
- Improve HTTP ingress channel performance, use appropriate worker threading
- Add data acquisition channel using CSV over HTTP for single and bulk readings
- Make CSV import format compatible with data from Open Hive and Beelogger. Cheers Clemens and Markus!
- Grafana Dashboard builder subsystem

    - Improve robustness
    - Add new fields to existing panels on demand. Thanks, Smilie!
    - Improve panel generator for :ref:`vendor-hiveeyes`

- Refactor data transformation machinery subsystems
- Add API endpoints and routing for creating timeseries annotations
- Start introducing :ref:`MQTT content type signalling <hiveeyes:topology-spec-0.2>`
- Drop support for InfluxDB 0.8
- Verify compatibility against InfluxDB 1.1.1, see also:

    - https://docs.influxdata.com/influxdb/v1.1/administration/differences/
    - https://github.com/influxdata/influxdb/blob/master/CHANGELOG.md#v111-2016-12-06

- Verify compatibility against Grafana 4.1.1, see also:

    - http://docs.grafana.org/guides/whats-new-in-v4/
    - http://docs.grafana.org/guides/whats-new-in-v4-1/
    - https://github.com/grafana/grafana/blob/master/CHANGELOG.md#411-2017-01-11

- Add ``mongod`` as Debian package dependency, required for CSV acquisition support

- Improve documentation
- Improve logging


.. _kotori-0.10.10:

2016-10-31 0.10.10
==================
- Fix Debian package re. superfluous “local” folder containing a redundant Python virtualenv. Thanks Smilie!
- Fix receiving discrete measurements via MQTT. Thanks Karsten and Clemens!
- Update Git repository url for hacking on Kotori
- Improve documentation


.. _kotori-0.10.9:

2016-07-12 0.10.9
=================
- Documentation updates, add system diagrams to vendor :ref:`vendor-hiveeyes`
- Export csv and json data with ISO format timestamps to satisfy dygraphs rendering in Firefox
- Don't add "pad=true" or "backfill=true" when "interpolate=true" parameter was obtained from URL
- Improve robustness of http api parameter evaluation and passing
- Improve Vega asset loading: Use https resources, better safe than sorry
- Add export format ".tsv" (text/tab-separated-values)


2016-07-10 0.10.7
=================
- Update documentation
- Rebuild without having "ggplot" installed on the build host


2016-07-10 0.10.6
=================
- Fix timeseries plotting by using “pad” and “backfill” appropriately
- Add export parameters "exclude", "include", "interpolate" and "sorted"
- Fix data routing and processing
- Add license to documentation
- Quick hack for making firmware builder endpoint no convert numeric values to floats
- Packaging fixes


.. _kotori-0.10.5:

2016-07-05 0.10.5
=================
- Attempt to fix huge dependency chain when installing with --install-recommends --install-suggests


2016-07-05 0.10.4
=================
- Fix missing runtime dependency "simplejson" (required by cornice)


2016-07-02 0.10.3
=================
- Use matplotlib “agg” backend
- Improve ggplot rendering context, add font for rendering xkcd theme
- Upgrade to pandas 0.18.1


2016-07-02 0.10.2
=================
- Honor https scheme in reverse proxy setups
- Packaging: Remove Python dependency on crossbar, can be installed through ``pip install crossbar==0.13.0``
- Packaging: Depend on more distribution packages to reduce package size


2016-07-01 0.10.1
=================

Packaging
---------
- Fix Debian runtime dependencies

Data export
-----------
- Always emit lowercase values from ``WanBusStrategy.sanitize_db_identifier()``
- When querying InfluxDB, quote table name (series/measurement) if identifier starts with a numeric value
- Add "exclude" parameter to HTTP API for mitigating scaling/outlier problems when plotting
- Fix "Excel worksheet name must be <= 31 chars." by introducing "compact" title


.. _kotori-0.10.0:

2016-06-29 0.10.0
=================
- Flexible InfluxDB data export and plotting machinery through HTTP,
  see :ref:`data-export` and :ref:`forward-http-to-influx`.
- Some words about the background and configuration of the firmware builder.


.. _kotori-0.9.0:

2016-06-17 0.9.0
================
- Add :ref:`firmware-builder` for automated builds
  of Arduino projects for vendor :ref:`vendor-hiveeyes`.


.. _kotori-0.8.0:

2016-06-06 0.8.0
================

General
-------
- Add HTTP-to-MQTT protocol forwarder component, see :ref:`forward-http-to-mqtt`
- Add Terkin PHP, a HTTP API library for :ref:`daq-php`, supports PHP5 and PHP4
- Relocate configuration blueprints in etc/examples

Bugfixes
--------
- Update default credentials for Grafana 3.x compatibility (admin/admin)
- Start HTTP server service only once, even when having multiple HTTP-to-X forwarders defined

Documentation
-------------
- Improve: Software releasing, package building and publishing. Both amd64 and armhf.
  See :ref:`kotori-release`, :ref:`kotori-build` and :ref:`setup-debian`.
- Improve: :ref:`getting-started`, :ref:`vendor-hiveeyes` and :ref:`setup-arch-linux`
- Add licenses AGPL 3.0 and EUPL 1.2
- Start :ref:`grafana-handbook` and :ref:`kotori-handbook` with appropriate clients
- Improve :ref:`application-mqttkit`
- Add :ref:`sawtooth-signal`
- Add :ref:`mosquitto-on-osx`
- Various improvements across the board
- Add a whole section about :ref:`data-acquisition` to the handbook providing
  a tour around the different ways to transmit telemetry data.
  This is Terkin in the belly of Kotori.


.. _kotori-0.7.1:

2016-05-22 0.7.1
================
- Update default credentials for Grafana 3.x in Kotori configuration (admin/admin)


2016-05-22 0.7.0
================

Vendor :ref:`vendor-hiveeyes`
-----------------------------
- Integrate and absorb communication style and subsystems of :ref:`vendor-hiveeyes`/:ref:`beradio` into core
- Refactor into generic Twisted service *MqttInfluxGrafanaService*,
  then implement the :ref:`vendor-hiveeyes` vendor application on top of it

Vendor :ref:`vendor-lst`
------------------------
- Improve command line tooling per ``lst-message <channel> info``:
  Display common information about a data channel like the
  configuration object and the names of all structs.
- Improve logging and debugging
- Optionally put legend on the right hand side of the graph

General
-------
- Improve configuration, logging, debugging and documentation
- Improve internal settings handling and application bootstrapping
- Introduce service-in-service infrastructure
- Make default Grafana panel not use ``steppedLines: true``,
  smooth lines are more beautiful when displaying sine curves
- Add *MqttKitApplication*, a generic application modeled after
  and using the :ref:`vendor-hiveeyes` vendor infrastructure
- Add *PahoMqttAdapter*: Migrate from `twisted-mqtt`_ to the
  *Eclipse Paho MQTT Python client library* `paho-mqtt`_,
  to enable running more than one MQTT adapter instance
- Introduce concept of "applications", which are native Twisted services
  and can be bootstrapped by defining them in the configuration file
- Add composite application completely declared by configuration settings
- Adapt :ref:`vendor-hydro2motion` and :ref:`vendor-lst` to infrastructure changes
- Upgrade libraries Twisted, autobahn, crossbar, msgpack and influxdb
- Improve Grafana gracefulness when finding a corrupt panel
- Overhaul configuration subsystem
- Try to reconnect to MQTT broker in interval if initial connection fails
- Add license, improve packaging and package publishing

Documentation
-------------
- Document how to :ref:`run-on-pypy`
- Improve documentation at :ref:`kotori-about` and :ref:`kotori-readme`
- Add CSS3 Hexagon Buttons 1.0.1 and more static assets
- Add Entypo pictograms by Daniel Bruce


2016-03-27 0.6.0
================

Vendor :ref:`vendor-lst`
------------------------
- resolve collision on parsed C header files when using identical filenames for different channels
- add project "proptest"

Vendor :ref:`vendor-hiveeyes`
-----------------------------
- improve configuration file “hiveeyes.ini” and logging
- fix Grafana panel creation re. Grafana 2.6.0 compatibility, Grafana 2.1.3 still works though
- fix Grafana panel creation re. InfluxDB select expression
- don’t put global realm “hiveeyes” into Grafana dashboard name
- improve Grafana panel automation
- accept single values on mqtt topic
- tune the default Grafana dashboard and panel
- documentation updates

Packaging
---------
- Modularize python dependencies into extra features
- Debian packaging using FPM

    - Read designated package version from setup.py
    - Use virtualenv-tools for relocating virtualenvs
    - Add systemd service configuration file

Miscellaneous
-------------
- Documentation refactoring and improvements


2015-11-26 0.5.1
================
- overhaul configuration files, activate “hydro2motion” channel with vendor :ref:`vendor-lst`
- fix hydro2motion re. database authentication
- lst: improve documentation


2015-11-26 0.5.0
================

Vendor :ref:`vendor-lst`
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

Proof-of-concept for vendor :ref:`vendor-lst`
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

General improvements
--------------------
- add release and documentation infrastructure through Makefile targets
- fix panel generation for vendor hiveeyes
- use nanosecond time precision with InfluxDB
- lst: honour struct field order in Grafana
- add more details to Grafana dashboard panels
- improve error messages “h2m-message send/decode”
- generalize c library adapter, multi-project capabilities for vendor lst


.. _Kotori 0.3.2:

2015-11-06 0.3.2
================

Proof-of-concept for vendor :ref:`vendor-hiveeyes`
--------------------------------------------------
- upgrade foundation libraries: Twisted, Autobahn, Crossbar
- receive messages via MQTT and store data points into InfluxDB
- storage: add support for InfluxDB 0.9
- storage: minor tweaks to enable influxdb database authentication
- receive telemetry data from BERadio
- grafana datasource- and dashboard automation
- Sort "collect_fields" result before passing to grafana manager

Vendor :ref:`vendor-hydro2motion`
---------------------------------
- refactor hydro2motion code

User interface
--------------
- add frontend foundation based on Pyramid web framework
- add jQuery, Bootstrap, Fontawesome, html5shiv and respond.js
- add material design for bootstrap
- add prototype html based on SB Admin 2 bootstrap template
- add modernizr and underscore
- add foundation for page transitions from codrops
- http: cache really static resources longer than volatile ones
- ui: add pages with page transitions, about content, etc.

General improvements
--------------------
- refactor project layout
- use configuration file instead of hardcoded configuration values
- improve logging


2015-05-21 0.2.2
================
- hydro2motion: production improvements from May 2015 in Rotterdam


2015-05-01 0.2.1
================

Vendor :ref:`vendor-hydro2motion`
---------------------------------
- ui: set map position to Munich
- ui: add lat long conversion
- backend: use InfluxDB on localhost
- backend: process complete Fuelcell telemetry data package


2015-04-24 0.2.0
================

Proof-of-concept for vendor :ref:`vendor-hydro2motion`
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

Proof-of-concept for vendor :ref:`vendor-ilaundry`
--------------------------------------------------
- Two daemons: master service and node service
- Communication infrastructure on top of Autobahn using PubSub
- Text-to-speech on top of Google Translate TTS
- Basic HTML Dashboard GUI for sending text messages

