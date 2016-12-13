.. include:: ../_resources.rst

.. _kotori-tasks:

############
Kotori tasks
############

.. contents::
   :local:
   :depth: 1

----

****
2016
****


2016-12-13
==========
- HTTP: Send timezones per channel
- HTTP: Get current list of header names
- HTTP: Announce value units
- Make MongoDB address configurable


2016-12-07
==========
- Add reading to panel on a per-field level
- Improve acquisition documentation
- CSV Bulk acquisition, re. timestamp
- FTP CSV acquisition
- Geohash
- CSV: What about quotes (")?
- "influxdb.exceptions.InfluxDBClientError: 400: write failed: field type conflict: input field "time" on measurement "area_42_node_1" is type string, already exists as type float"
- How to signal errors occurring in the data acquisition chain?
- Use dateutil.parse immediately on HTTP ingress, so UTC will be republished to MQTT
- Remember whether InfluxDB database already was created to prevent hammering
- Hiveeyes / Open Hive CSV:
    - Spannung auf separatem Panel
- How to provide the user with access to the log file?
  e.g. for error messages like ``influxdb.exceptions.InfluxDBClientError: 400: {"error":"unable to parse 'area_42_node_7  1474570699000000000': invalid field format"}``
- How to run the metrics LoopingCall to actually work when the system is under load?


2016-12-02
==========
- | Ponte is a multi-transport Internet of Things / Machine to Machine broker.
  | As the current state it supports MQTT and REST APIs over HTTP and CoAP.
  | https://github.com/eclipse/ponte
- http://learninginternetofthings.com/bottlenecks-coap-mqtt/
- | CoAP observe
  | https://tools.ietf.org/html/rfc7641
- | MongoDB on ARM
  | https://github.com/Barryrowe/mongo-arm
  | https://raspberrypi.stackexchange.com/questions/22404/official-mongodb-repo-for-arm-processor-for-debian-base
  | http://andyfelong.com/2016/05/mongodb-3-2-6-running-under-arch-linux-arm-64-bit/
- | http://www.reder.eu/
  | http://www.domoticshop.eu/Flyer/BETTY_schreibt_mit.pdf


2016-11-17
==========
- Geodata and timestamping
- CSV Telemetry
- FTP Upload
- Timeslider-based replay of recorded information (esp. geo)
- Scheduled aggregation report notifications with mqttwarn.
  See http://tinkerman.cat/mqtt-topic-naming-convention/
- Jan-Piet Mens tweeted about Kotori, thanks!

    - https://twitter.com/jpmens/status/798888207110770689
    - Some people liked it:

        - https://twitter.com/Diorf
        - https://twitter.com/roundtripdelay


2016-11-13
==========
- Integrate with re:dash?

    - https://redash.io/
    - https://github.com/getredash/redash

- Integrate with open source IFTTT clone?

    - Trigger Happy: https://trigger-happy.eu/
    - Huginn: https://github.com/cantino/huginn


2016-11-12
==========
- Review emails re. requirements from environmental monitoring project of Freifunk Berlin
- Use Grafana Worldmap panel

    - https://github.com/grafana/worldmap-panel/issues/9
    - https://github.com/grafana/worldmap-panel/issues/30

- Add ~/dev/dosyit/rotor-timeseries


Docs
----
- Web search for "open source data historian"

    - http://www.minaandrawos.com/2015/11/20/thoughts-on-process-historians/
    - https://coussej.github.io/2016/04/18/Building-An-Open-Source-Process-Historian/
    - https://github.com/coussej/node-opcua-logger

- More "open source data historian"

    - https://openhistorian.codeplex.com/
    - https://github.com/GridProtectionAlliance/openHistorian
    - http://discussions.gridprotectionalliance.org/t/openpdc-to-mysql-database/70
    - https://github.com/GridProtectionAlliance/PQDashboard
    - http://openscada.org/
    - https://eclipse.org/eclipsescada/
    - https://eclipse.org/eclipsescada/news.html
    - http://openscada.org/projects/atlantis
    - http://openopc.sourceforge.net/
    - http://www.controlconsulting.com/products/data-historian/
    - https://github.com/volkszaehler/
    - https://github.com/volkszaehler/vzlogger
    - http://wiki.volkszaehler.org/software/controller/vzlogger
    - http://blog.canarylabs.com/2016/06/a-guide-to-best-data-historian-software.html

- Format case studies like on http://rundeck.org/
- http://www.hivemq.com/mqtt-essentials/
- https://blog.hypertrack.io/2016/11/10/how-we-ditched-http-and-transitioned-to-mqtt/


2016-11-11
==========
- | MQTT Node-RED flow
  | https://www.domoticz.com/forum/viewtopic.php?t=838&start=120
- https://vrm.victronenergy.com
- | Bidirectional traffic between CCGX D-Bus and MQTT broker
  | https://github.com/wiebeytec/dbus-mqtt
- https://www.pubnub.com/
- https://github.com/flukso/lua-mosquitto


2016-11-04
==========
- Grafana dashboard creation: NODE=HUZZAH,GW=DACH,NET=KH.
  Improve when sending from a different node: node=feather,gw=wormcompost.
- http://www.mqtt-dashboard.com/


2016-11-01
==========
- Improve situation of the Python/MQTT client. Describe how to add timestamp
  and geohash to provide temporal and spatial information from sensor nodes.
- First experiments with https://tsfresh.readthedocs.io/


2016-10-30
==========
- Add Kotori to https://github.com/hobbyquaker/awesome-mqtt


2016-10-27
==========
- Introduce ZeroMQ data acquisition


2016-10-08
==========
- Call out to IFTTT, e.g. https://github.com/ubirch/ubirch-board-examples/blob/master/src/gsm_console/call.txt
- https://github.com/jpmens/mqttwarn/issues/78


2016-10-06
==========
- https://www.movebank.org/node/5788
- https://www.movebank.org/node/34
- https://www.movebank.org/node/15294


2016-10-05
==========
- Trigger IFTTT event, e.g. http://maker.ifttt.com/trigger/hum_alarm/with/key/nh6E
- Annotations, finally! http://maxchadwick.xyz/blog/grafana-influxdb-annotations

    - curl -X POST "http://localhost:8086/write?db=mydb&precision=s" --data-binary 'events title="Deployed v10.2.0",text="<a href='https://github.com'>Release notes</a>",tags="these are the tags" 1470661200'
    - SELECT title, tags, text FROM events WHERE $timeFilter


2016-10-03
==========

MongoDB on ARM
--------------
- https://jira.mongodb.org/browse/SERVER-1811
- https://github.com/Barryrowe/mongo-arm
- http://raspberrypi.stackexchange.com/questions/22404/official-mongodb-repo-for-arm-processor-for-debian-base
- http://www.clarenceho.net/2015/12/building-mongodb-30x-for-arm-armv7l.html
- http://andyfelong.com/2016/01/mongodb-3-0-9-binaries-for-raspberry-pi-2-jessie/
- http://andyfelong.com/2016/05/mongodb-3-2-6-running-under-arch-linux-arm-64-bit/
- http://downloads.mongodb.org/linux/mongodb-linux-arm64-ubuntu1604-3.3.15.tgz


2016-09-30
==========
BMBF „Open Photonik“

- http://maker-faire.de/berlin/auftaktveranstaltung-open-photonik/
- http://www.photonikforschung.de/innovationsunterstuetzung/
- http://www.photonikforschung.de/forschungsfelder/open-innovation/open-photonik/
- https://sensebox.de/


2016-09-21
==========
- Have a look at Metabase:

    - http://www.metabase.com/
    - https://github.com/metabase/metabase


2016-09-14
==========
- Docs: Add "contact" page
- Docs: Add "How to configure (and secure) Nginx" or how to bind HTTP port to *:24642.


2016-09-09
==========
- | https://github.com/mwasilak/txThings
  | https://github.com/chrysn/aiocoap
  | https://twistedmatrix.com/pipermail/twisted-python/2013-September/027453.html
  | http://www.sixpinetrees.pl/
- | http://riot-os.org/
  | https://github.com/RIOT-OS/RIOT
  | https://github.com/crossbario/autobahn-c/issues/8
- https://github.com/nikipore/stompest
- WebIOPi (coap)
    - http://webiopi.trouch.com/
    - http://trouch.com/about/
    - https://twitter.com/eptak
    - https://www.linkedin.com/in/eric-ptak-91204816
    - http://trouch.com/
    - http://webiopi.trouch.com/
    - http://www.cayenne-mydevices.com/landing/create-raspberry-pi-projects-with-cayenne/
    - http://www.cayenne-mydevices.com/Supported-Hardware/
    - http://blog.mydevices.com/
    - https://developer.weaved.com/portal/
    - https://www.weaved.com/raspberry-pi-remote-connection/



2016-09-05
==========
- http://www.gantner-instruments.com/
- https://home-assistant.io/
- New Logo for Mosquitto

    - http://mosquitto.org/stickers/
    - https://en.99designs.fr/logo-design/share/34547/6f0be6
    - http://mosquitto.org/2016/05/stickers/


2016-07-14
==========
- [o] Earthship monitoring: https://github.com/ma-tri-x/ESpy


2016-07-12
==========
- [x] Add export format ".tsv"
- [o] Improve resiliency when InfluxDB or Grafana is down
- [o] Disable request.site.displayTracebacks on production
- [o] Vendor Hiveeyes: Integrate wq.io for Stockkarte


2016-07-11
==========
- [x] Plotting does not work for:

    - https://swarm.hiveeyes.org/api/hiveeyes/25a0e5df-9517-405b-ab14-cb5b514ac9e8/3756782252718325761/1/data.dy?exclude=wght1&from=20160519T040000&to=20160519T170000
      => Does not work in Firefox due to errors like "Couldn't parse 2016-05-19 04:04:29.390000128 as a date dygraph-combined.js:4:3438"
    - https://swarm.hiveeyes.org/api/hiveeyes/25a0e5df-9517-405b-ab14-cb5b514ac9e8/3756782252718325761/1/data.dy?exclude=wght1&from=20160519T040000&to=20160519T170000&interpolate=true
      => Don't add "pad=true" or "backfill=true" when "interpolate=true" or other parameters were obtained from URL
    - https://swarm.hiveeyes.org/api/hiveeyes/25a0e5df-9517-405b-ab14-cb5b514ac9e8/3756782252718325761/1/data.vega?exclude=wght1&from=20160519T040000&to=20160519T170000
      => [...] was loaded over HTTPS, but requested an insecure script 'http://d3js.org/d3.v3.min.js'


2016-07-10
==========
- [o] Document export parameters "exclude", "include", "interpolate" and "sorted"


2016-07-06
==========
- [o] http://www.rocketscream.com/blog/2016/03/10/radio-range-test-with-rfm69hcw/
- [o] Export data to http://orange.biolab.si/


2016-07-05
==========
- [x] Float is not iterable when querying with "&from=20160101"
- [x] Also provide ?include=temp1,temp2,... parameter to data export interface doing the reverse of ?exclude=wght2
- [o] Packaging: When doing ``make debian-package flavor=daq``, if Kotori is not installed in /opt/kotori::

      make[1]: /home/workbench/isarengineering/kotori/build/kotori/bin/pip: Command not found

  Reason::

      #!/opt/kotori/bin/python

- [o] Packaging: Do ``rm dist/*.deb`` after uploading successfully
- [o] Annotations, finally: http://lkhill.com/using-influxdb-grafana-to-display-network-statistics/
- [o] Use Holt-Winters to predict data: https://docs.influxdata.com/influxdb/v1.0/query_language/functions/#holt-winters
- [o] Javascript wrapper for HTTP API on top of https://github.com/jpillora/jquery.rest
- [o] Optionally use "from pyinfluxql.functions import Mean" in protocol/influx.py


2016-07-04
==========
- [o] Allow deployment using Docker, see
  https://community.openenergymonitor.org/t/emoncms-docker-run-emoncms-on-your-machine-in-4-commands/823


2016-07-02
==========
- [x] Problem with simplejson after installing

When building for the first time::

    B /home/workbench/isarengineering/kotori/build/kotori/lib/python2.7/site-packages/cornice/scaffolds/__init__.pyc
    Traceback (most recent call last):
      File "/home/workbench/isarengineering/kotori/build/kotori/bin/virtualenv-tools", line 9, in <module>
        load_entry_point('virtualenv-tools==1.0', 'console_scripts', 'virtualenv-tools')()
      File "/home/workbench/isarengineering/kotori/build/kotori/lib/python2.7/site-packages/virtualenv_tools.py", line 258, in main
        if not update_paths(path, options.update_path):
      File "/home/workbench/isarengineering/kotori/build/kotori/lib/python2.7/site-packages/virtualenv_tools.py", line 187, in update_paths
        update_pycs(lib_dir, new_path, lib_name)
      File "/home/workbench/isarengineering/kotori/build/kotori/lib/python2.7/site-packages/virtualenv_tools.py", line 140, in update_pycs
        update_pyc(filename, local_path)
      File "/home/workbench/isarengineering/kotori/build/kotori/lib/python2.7/site-packages/virtualenv_tools.py", line 96, in update_pyc
        code = marshal.load(f)
    ValueError: bad marshal data (unknown type code)


2016-07-01
==========
- [x] Fix numpy runtime dependency on atlas, PyTables runtime dependency on HDF5 and more::

    exceptions.ImportError: Missing required dependencies ['numpy']
    ImportError: libf77blas.so.3: cannot open shared object file: No such file or directory

    [...]

    ImportError: HDFStore requires PyTables, "libhdf5_serial.so.8: cannot open shared object file: No such file or directory" problem importing

  aptitude install -y libatlas-base-dev libopenblas-base liblapack3 libhdf5-8 libnetcdfc7 liblzo2-2 libbz2-1.0
  aptitude install -y libpng12-0 libfreetype6 python-cairocffi

- [x] Add .lower() conversion to WanBusStrategy.sanitize_db_identifier
- [x] Add quotes to series name when querying InfluxDB series starting with numeric value, e.g. 3756782252718325761_1
- [x] Add "exclude" parameter for mitigating scaling/outlier issue with "wght1", e.g.
  https://swarm.hiveeyes.org/api/hiveeyes/25a0e5df-9517-405b-ab14-cb5b514ac9e8/3756782252718325761/1/data.png?renderer=ggplot&from=20160519T040000&to=20160519T170000
- [x] Fix exceptions.Exception: Excel worksheet name '25a0e5df_9517_405b_ab14_cb5b514ac9e8_3756782252718325761_1' must be <= 31 chars.
- [x] Check if build dependencies can be announced to fpm
- [o] Investigate void rendering with:
  https://swarm.hiveeyes.org/api/hiveeyes/25a0e5df-9517-405b-ab14-cb5b514ac9e8/3756782252718325761/1/data.png?from=20160519T040000&to=20160519T170000
- [o] Build packages for armhf
- [o] cairo: no  [cairocffi or pycairo not found]
- [o] PyTables: Could not find blosc headers and library; using internal sources.
- [o] Add logrotate configuration
- [o] Dependency Links processing has been deprecated with an accelerated time schedule and will be removed in pip 1.6
- [o] matplotlib has 50MB on its own, can't we just depend on python-matplotlib? (and python-numpy, and python-pandas?)
- [o] make -j4 when building package


2016-06-25
==========
- [o] Data export
    - [x] Run export machinery in seperate thread
    - [x] Care for runtime exceptions in export machinery
    - [x] Properly format "data.csv" download name
    - [x] Integrate Bokeh renderer
    - [x] Refactor dygraphs, Bokeh and Vincent renderers to UniversalPlotter
    - [x] Get rid of "bus/mqtt" in documentation of other HTTP handlers
    - [o] Index page for GET ../data displaying all available formats
    - [o] Properly handle units in graphs
    - [o] Load Bokeh data via json
    - [o] Suppress spontaneous Twisted-rendered stacktraces
    - [o] Self-host static assets like dygraphs, jquery, etc. (from UniversalPlotter)
    - [o] Convert more formats using Odo
      http://odo.pydata.org/en/latest/json.html
    - [o] More tabular renderings e.g. using https://pypi.python.org/pypi/PrettyTable and https://github.com/6pac/SlickGrid
      See also:
        - http://clusterize.js.org/
        - https://stackoverflow.com/questions/2402953/javascript-data-grid-for-millions-of-rows/8831087#8831087

    - [o] More visualizations, see also: https://tomaugspurger.github.io/modern-6-visualization.html
    - [o] More scientific data formats, see also:

        - http://docs.scipy.org/doc/scipy/reference/io.html
        - http://stackoverflow.com/questions/19134317/find-all-differences-between-mat-files

    - [o] Mixed data types in HDF5: https://github.com/pydata/pandas/issues/3032
    - [o] Branding for HTML-based output (e.g. for Hiveeyes / Open Hive)
    - [o] Insert user block into HDF5 file using appropriate API methods like h5jam/h5unjam

- [o] Data routing: Flexible MQTT topic republishing


2016-06-06
==========
- [o] Add Javascript and Arduino clients (using HTTP+JSON)
- [o] Package building: /COPYRIGHT and /LICENSE get introduced from crossbar


2016-06-05
==========
- [o] Check whether "Export" functionality could be built on top of a Grafana data source

    - https://docs.influxdata.com/influxdb/v0.13/query_language/data_exploration/#relative-time

    - https://swarm.hiveeyes.org/grafana/api/datasources/proxy/10/query?db=hiveeyes_25a0e5df_9517_405b_ab14_cb5b514ac9e8&q=%3BSELECT%20%22temp3%22%20FROM%20%223756782252718325761_1%22%20WHERE%20time%20%3E%201463630400s%20and%20time%20%3C%201463677200s&epoch=ms

    - | time > '2016-05-19 04:00:00'  and time < '2016-05-19 17:00:00'
      | time > '2016-05-19T04:00:00Z' and time < '2016-05-19T17:00:00Z'
      | https://swarm.hiveeyes.org/grafana/api/datasources/proxy/10/query?db=hiveeyes_25a0e5df_9517_405b_ab14_cb5b514ac9e8&q=%3BSELECT%20%22temp3%22%20FROM%20%223756782252718325761_1%22%20WHERE%20time%20%3E%20%272016-05-19%2004:00:00%27%20and%20time%20%3C%20%272016-05-19%2017:00:00%27&epoch=ms

    - | now() - 30d
      | https://swarm.hiveeyes.org/grafana/api/datasources/proxy/10/query?db=hiveeyes_25a0e5df_9517_405b_ab14_cb5b514ac9e8&q=%3BSELECT%20%22temp3%22%20FROM%20%223756782252718325761_1%22%20WHERE%20time%20%3E%20now()%20-%2030d&epoch=ms


    - | now() - 30d
      | https://swarm.hiveeyes.org/grafana/api/datasources/proxy/10/query?db=hiveeyes_25a0e5df_9517_405b_ab14_cb5b514ac9e8&q=SELECT * FROM /.*/ LIMIT 1&epoch=ms


    - ::

        The other options for specifying time durations with now() are listed below.
        u microseconds
        ms milliseconds
        s seconds
        m minutes
        h hours
        d days
        w weeks


- [o] Add :ref:`HTTPie <daq-httpie>` example directly into ``http-to-mqtt.ini`` (:ref:`forward-http-to-mqtt`)


2016-06-04
==========

Forwarders
----------
- Protocol adapters

    - http-to-mqtt
    - mqtt-to-wamp
    - udp-to-mqtt

- Data querying and export

    - http-to-influxdb

- Clients (library and examples: demo, sawtooth)

    - Bash
    - Python
    - PHP

- Uniform example program interfaces::

    kotori-client.(sh|py|php) transmit demo
    kotori-client.(sh|py|php) transmit sawtooth
    kotori-client.(sh|py|php) fetch demo

- Documentation!

- Clients (universal CLI) => Terkin?

; Todo:     Add predicate for verifying the payload actually is in JSON format, e.g.::
;
;               source_predicate = body.format:json
;
;           Or by directly defining Python code as validator, e.g.::
;
;               source_predicate = json.loads(body)
;


Misc
----
- [o] Recursively read configuration files
- [o] Generalize metrics subsystem and add to different applications


2016-05-27
==========
- [o] Notify jpmens about handbook/acquisition/sawtooth.html#multiple-sawtooth-signals,
  also write something about "jo" at https://blog.simeonov.com/2014/01/21/manipulating-json-jsonlines-command-line/

- [o] Connect from an ESP8266::

    [10] https://harizanov.com/2015/11/rfm69-to-mqtt-gateway-using-esp8266/
    [11] https://github.com/someburner/esp-rfm69
    [12] https://github.com/someburner/esp-rfm69/wiki/MQTT
    [13] http://tuanpm.net/native-mqtt-client-library-for-esp8266/
    [14] https://github.com/tuanpmt/esp_mqtt
    [15] https://hiveeyes.org/docs/beradio/research/mqtt.html#c

- [o] Also have a look at::

    [4] http://www.esp8266.nu/index.php/ESPEasy
    [5] https://github.com/ESP8266nu/ESPEasy
    [6] http://www.esp8266.nu/index.php/EasyProtocols
    [7] http://www.esp8266.nu/index.php/EasyOTA
    [8] https://github.com/ESP8266nu/ESPEasySlaves
    [9] https://github.com/ESP8266nu/ESPEasySlaves/blob/master/MiniProExtender/MiniProExtender.ino

- [o] Build and document Kotori CoAP interface based on txThings
- [o] Q: ``Uncaught SecurityError: Failed to read the 'localStorage' property from 'Window': Access is denied for this document.``

    - Detect whether Grafana from foreign domain could not be included, check
      https://www.chromium.org/for-testers/bug-reporting-guidelines/uncaught-securityerror-failed-to-read-the-localstorage-property-from-window-access-is-denied-for-this-document

- [o] Disable Grafana refreshing for static graphs w/o live data on pages like :ref:`sawtooth-signal`.


2016-05-26
==========
- [o] Add proper content attributions to media elements from 3rd-party authors
- [o] Display license in documentation
- [o] By default (mqttkit), prefix dashboard names with realm, to avoid collisions like with hiveeyes.
- [o] Default zoom level for new Grafana dashboards should be "Last 5 minutes" or even shorter

2016-05-25
==========
- [o] Hiveeyes needs a different activity indicator in log file due its low transmission rate. Introduce total packet counter.
- [o] Slogan: Data acquisition without friction.

2016-05-24
==========
- [x] Upload InfluxDB 0.13.0 from https://influxdata.com/downloads/#influxdb to package repository
- [o] Create meta package "kotori-bundle"
- [o] For querying InfluxDB, use PyInfluxQL: https://github.com/jjmalina/pyinfluxql


2016-05-23
==========
- [o] Build packages for other distributions. e.g. CentOS, SuSE, Arch Linux using ``alien``.
- [o] Improve :ref:`application-mqttkit`

    - How to use apps-available vs. apps-enabled

- [o] Improve ``applications/index.rst``: Add more pictures
- [o] Redirect https://hiveeyes.org/docs/kotori/ to https://getkotori.org/docs/
- [o] Grafana: Multi-panel dashboard-solo
- [o] Publish CHANGES.rst to debian/changelog


2016-05-22
==========
- [o] Adapt python source egg publishing location, upload to PyPI
- [o] Publish current InfluxDB and Grafana packages along with Kotori. Streamline :ref:`setup-debian`.
- [o] Add /etc/default/kotori to Debian package
- [o] Build and add ARM packages to Debian repository
- [o] Add README.rst, CHANGES.rst, LICENSE*.txt and agpl-3.0.txt to Python- and Debian packages, check

    - https://stackoverflow.com/questions/9977889/how-to-include-license-file-in-setup-py-script
    - https://programmers.stackexchange.com/questions/234511/what-is-the-best-practice-for-arranging-third-party-library-licenses-paperwork/234526#234526

- [o] Prevent "useradd: user 'kotori' already exists" when upgrading package
- [o] Activate email address "support@getkotori.org"
- [o] Add contributors and credits to documentation
- [o] Regularly check for new foundation packages

    - https://s3.amazonaws.com/influxdb/
    - https://packagecloud.io/grafana/stable
    - https://github.com/fg2it/grafana-on-raspberry

- [o] Change GPG key passphrase on production package publishing host


2016-05-21
==========
- [o] Add Grafana graphs to applications/hiveeyes.rst


2016-05-20
==========
- [o] Integrate with https://collectd.org/documentation/manpages/collectd.conf.5.shtml#plugin_barometer
- [o] HiveeyesDaily summary report
- [o] MqttWampBridge for LST-MAVLINK
- [o] Pyramid refactoring
- [o] Minimal dashboard plugin system
- [o] Compile individual firmwares directly from git repository
- [o] Improve package building and releasing
- [o] Upgrade Python dependencies to recent versions


2016-05-18
==========
- [o] Integrate with AWS IoT Button
    - https://aws.amazon.com/iot/button/
    - https://news.ycombinator.com/item?id=11687463
- [o] Package as "SNAP": https://wiki.ubuntu.com/XenialXerus/ReleaseNotes#Snap_application_format


2016-05-13
==========
- [o] Improve MQTTKit documentation
- [o] ==> /var/log/kotori/kotori.log <==
      2016-05-13T18:50:51+0200 [kotori.daq.graphing.grafana        ] WARN: Unable to format event {'log_namespace': 'kotori.daq.graphing.grafana', 'log_level': <LogLevel=warn>, 'log_logger': <Logger 'kotori.daq.graphing.grafana'>, 'log_time': 1463158251.727876, 'log_source': None, 'log_format': u'Client Error 404: {"message":"Dashboard not found"}'}: u'"message"'
- [o] kwargs={'userdata': {'foo': 'bar'}
- [o] Convenience alias for "utc"


2016-05-04
==========
- [o] Issues after installing Kotori-0.5.0 from Debian package

    - | tabulate,pyclibrary,sympy muß noch via pip in venv.
      | => pip install kotori[daq_binary]
    - | die dateien fehlen: /opt/kotori/lib/python2.7/site-packages/kotori/daq/graphing/resources/grafana-dashboard.json ...
      | ERROR: IOError: [Errno 2] No such file or directory: '/opt/kotori/lib/python2.7/site-packages/kotori/frontend/development.ini'
    - | [04.05.16 00:23:33] Janosch: ahh ja nochwas. irgendwie hat er die rechte nicht richtig gesetzt auf /opt/kotori.
      | er hat 1000 genommen obwohl er 1001 ist.
      | evtl aber auch erst nachdem ich ein dpkg -p kotori und nochmal ein dpkg -i ....
      | [04.05.16 00:23:54] Janosch: muß man auch nochmal überprüfen
    - | Disable Grafana completely or reduce error logging: In a situation where the credentials do not match,
      | this would otherwise (currently) cause an exception storm of Grafana communication failures.

- [o] InfluxDB 0.12.0 requires Grafana 3: https://github.com/influxdata/influxdb/issues/6220

- [o] Docs about how to

    - send telemetry data to generic MQTTKit application (mosquitto_pub, Python)
    - store InfluxDB payloads to database

- [o] Configuration setting to disable Grafana completely

- [o] Vendor "LST"

    - Add metrics
    - Don't use the WAMP bus for achieving higher performance (disable optionally)

- [o] Put files from etc/apps-available to etc/examples?


2016-04-22
==========
- [o] Integrate with AllSeen/AllJoyn: https://allseenalliance.org/framework/documentation/develop/building/linux


2016-04-18
==========
- [o] Revamp and improve the Hydro2Motion setup and infrastructure for a new round of `Shell Eco-marathon europe`_ 2016.


2016-04-17
==========
- Let's use the squirrel as a mascot for Terkin. Does the Skype emoticon ``(heidy)`` has a representation in Unicode?

    - http://users.skynet.be/sky77548/squirrel3.gif
    - https://thenounproject.com/term/squirrel/1326/
    - Favourites:

        - https://thenounproject.com/term/squirrel/83208/
        - https://thenounproject.com/term/squirrel/316333/


2016-04-13
==========
- RF69, RF95, RF212


2016-04-12
==========
- [o] Implement Terkin - the Kotori client - based on Click

    - http://click.pocoo.org/

- [o] Add more pictures (Hiveeyes, LST)

- [o] Add references to documentation

    - https://en.wikipedia.org/wiki/Bus_analyzer
    - https://en.wikipedia.org/wiki/Data_logger
    - https://en.wikipedia.org/wiki/Chart_recorder
    - https://de.wikipedia.org/wiki/Messschreiber

- [o] Integrate with http://www.byteparadigm.com/products/log-storm/
- [o] Integrate with taloLogger

    - http://olammi.iki.fi/sw/taloLogger/
    - http://olammi.iki.fi/sw/taloLoggerPi/
    - http://olammi.iki.fi/sw/taloLoggerGraph/

- [o] Make an OpenEmbedded layer for Kotori for integrating with Yocto

    - https://yoctoproject.org/
    - http://openembedded.org/
    - https://buildroot.org/
    - http://layers.openembedded.org/layerindex/branch/master/layers/
    - http://layers.openembedded.org/layerindex/branch/master/layer/meta-python/
    - http://layers.openembedded.org/layerindex/branch/master/layer/meta-web-kiosk/
    - http://layers.openembedded.org/layerindex/branch/master/layer/meta-talologger/
    - https://github.com/hlounent/meta-talologger


2016-04-11
==========
- [o] Integrate with http://dangerousprototypes.com/docs/Bus_Pirate
- [o] Altitude sensor http://dangerousprototypes.com/2016/04/11/using-bmp180-for-temperature-pressure-and-altitude-measurements/


2016-04-10
==========
- [o] Proper TLS/GPG key management for transports like HTTP, MQTT, etc.
- [o] Compatibility/integration with phant.io and analog.io
- [o] Add section about similar projects to the documentation
- [o] Signal processing with http://non.tuxfamily.org/ ?
- [o] The fine dashboard for Hydro2Motion: https://mryslab.github.io/rbDashBoard/
- [o] Integrate with Xideco_, see also

    - https://github.com/MrYsLab/xideco/tree/master/xideco/xidekit/xidekit_examples
    - http://mryslab.blogspot.de/
    - :ref:`vendor-ilaundry`


2016-04-06
==========
- [o] Get rid of "CREATE DATABASE" calls for each and every measurement
- [o] Improve InfluxDB connection resiliency if database is down on initial connect


2016-04-05
==========
- [o] LST:
    - Refactor components
        - UDPReceiver and UdpBusForwarder => UdpBusForwarder and UdpBusPublisher
        - WampApplication => WampBus
    - Automatically publish messages to the MQTT bus using composition of generic components
- [o] Refactor MqttInfluxGrafanaService and BusInfluxForwarder into
      new generic component and reuse at Hiveeyes/mqttkit and LST
- [o] Throughput metrics for vendor LST
- [o] Configuration and packaging for 0.7.0
- [o] Pyramid should go to kotori.web with frontend on port 4000
- [o] Introduce boot_frontend as kotori.web.mount(app=app, port=4000),
      where "app" might be "kotori.frontend:file://development.ini:main"
- [o] Inject kotori settings into options (to be used as global_conf)


2016-04-04
==========
- [o] MqttInfluxGrafanaService: Configure metrics to be collected each X seconds: Get from configuration with fallback to default of 60 seconds
- [o] Check fact if any errors occurred when booting and display periodically in log output
- [o] Use data sources of Crossbar.io, e.g. http://crossbar.io/iotcookbook/Arduino-Yun-Accelerometer/
- [o] Check out http://crossbar.io/iotcookbook/Arduino-Yun-Create-Image/
- [o] Check out http://robomq.io/

2016-04-03
==========
- [o] Introduce ``kosh``, the Kotori Shell

    - kosh show channels
    - kosh show subchannels
    - kosh show services

- [o] Make interval of periodic rate display configurable::

    2016-04-03T04:47:09+0200 [kotori.daq.services.mig            ] INFO: [hiveeyes] measurements: 0.00 Hz, transactions: 0.00 tps
    2016-04-03T04:47:09+0200 [kotori.daq.services.mig            ] INFO: [mqttkit] transactions: 0.00 tps

- [o] Fix threading bug when having multiple MQTT subscribers::

    2016-04-03T04:50:13+0200 [mqtt                               ] ERROR: Unexpected CONNACK packet received in None

  | Also, the TwistedMqttAdapter "mqtt-mqttkit" somehow seems to take over the **existing**
  | MQTT session of TwistedMqttAdapter "mqtt-hiveeyes" and receives all its messages. WTF!
  | => Try to migrate to *paho-mqtt*, in a multithreaded setup on top of ``client.loop_forever()`` for convenience.

- [o] Use TLS for MQTT connections
- [o] Improve log format: Put Python module namespace at the end of the line
- [o] Use timestamp from Paho if not supplied via data message
- [o] Add measurement count to INFO: [hiveeyes  ] measurements: 4.96 Hz, transactions: 5.00 tps
- [o] Start dogfeeding by subscribing to ``$SYS/#``
- [o] The realm does not get incorporated into the name of the Grafana dashboard::

    2016-04-03T22:26:09+0200 [kotori.daq.graphing.grafana        ] INFO: Provisioning Grafana for database "hiveeyes_3733a169_70d2_450b_b717_6f002a13716b" and series "tug22_999". dashboard=3733a169-70d2-450b-b717-6f002a13716b
    2016-04-03T22:26:09+0200 [kotori.daq.graphing.grafana        ] INFO: Creating datasource "hiveeyes_3733a169_70d2_450b_b717_6f002a13716b"
    2016-04-03T22:26:09+0200 [kotori.daq.graphing.grafana        ] INFO: Getting dashboard "3733a169-70d2-450b-b717-6f002a13716b"
    2016-04-03T22:26:09+0200 [kotori.daq.graphing.grafana        ] INFO: No missing panels to add


2016-03-30
==========
- [o] Blocking issue with twisted-mqtt

    - https://pypi.python.org/pypi/twisted-mqtt

maybe go to:

    - HBMQTT (MQTT client/broker using Python asynchronous I/O): https://github.com/beerfactory/hbmqtt
    - https://stackoverflow.com/questions/31899679/handling-async-in-python
    - https://twisted.readthedocs.org/en/latest/core/howto/threading.html
    - https://github.com/astrorafael/twisted-mqtt

- [o] Integrate with Belkin WeMo devices, see also

    - https://ouimeaux.readthedocs.org/
    - https://github.com/iancmcc/ouimeaux
    - https://www.domoticz.com/wiki/Wemo
    - http://concisionandconcinnity.blogspot.de/2013/02/ouimeaux-command-line-and-python-api.html

- [o] Papers

    - | BearLoc: A Composable Distributed Framework for Indoor Localization Systems
      | http://www.cs.berkeley.edu/~kaifei/data/iot-sys_15.pdf
    - | Developing Real Time Communication (RTC) Platform for IoT Using PubNub
      | https://dzone.com/articles/developing-real-time-communication-rtc-platform-fo-1
    - | Coupling Real Time Elements in the IoT: A Requirement to Reach Industry 4.0
      | https://www.digikey.com/en/articles/techzone/2015/jul/coupling-real-time-elements-in-the-iot-a-requirement-to-reach-industry-4-0

- [o] txThings: simple library for CoAP protocol

    - https://twistedmatrix.com/pipermail/twisted-python/2013-September/027453.html
    - https://github.com/mwasilak/txThings
    - http://www.sixpinetrees.pl/2013/09/txthings-good-enough-is-good-enough.html

- [o] Replace Kotori with mqttcollect? :-)
  http://jpmens.net/2015/05/15/an-exec-plugin-for-collectd-mqttcollect/

- [o] Watch TESS

    - https://testpypi.python.org/pypi/tessdb
    - https://github.com/astrorafael/tessdb/
    - http://www.observatorioremoto.com/TESS.pdf
    - http://www.observatorioremoto.com/



2016-03-29
==========
- [o] Documentation: Redesign root index.rst to use panels/boxes for displaying the different documentation sections
- [o] Get in touch with upstream projects

    - http://wamp-proto.org/

- [o] More logos for "About Kotori"
- [o] Coin the "MIG" stack
- [o] Refactor "Kotori goals" out of "About Kotori"
- [o] Documentation about Kotori clients

    - beradio-python, -lua, -cpp
    - mqttkit-python, -lua
    - mbed library

- [o] Alternative names for Kotori client:

    - m2mkit, m2mclient, m2mrequests
    - pargura, corello, semper, vimere, terkin, catrin, bangaro, camper, patron

- [o] Integrate with TESS

    - https://testpypi.python.org/pypi/tessdb
    - https://github.com/astrorafael/tessdb/
    - http://www.observatorioremoto.com/TESS.pdf

- [o] Coupling Real Time Elements in the IoT: A Requirement to Reach Industry 4.0 (2015-07-16)

    - https://www.digikey.com/en/articles/techzone/2015/jul/coupling-real-time-elements-in-the-iot-a-requirement-to-reach-industry-4-0

- [o] https://github.com/phodal/iot-document/blob/master/protocol/MQTT.lib.md
- [o] https://phodal.github.io/awesome-iot/


2016-03-28
==========
- [o] Document some performance data:

    - MQTT and InfluxDB

        - Python 2.7

            - measurements: 1000-1300 Hz
            - transactions: 50-70 tps   (30-40 tps when debugging)

        - PyPy 5.0

            - | measurements: 2000-3000 Hz
            - | transactions: 50-70 tps when ramping up, then goes down to 5-15 tps :-(
              | Q: What's the reason?
              | A: Probably because we don't have a thread pool on the storage adapter side yet
              |    and the number of parallel requests leads to contention on the Twisted side.

- [o] MqttWampBridge
- [o] InfluxDB, MQTT- and Grafana connection and operation robustness/resiliency
- [o] Run "CREATE DATABASE only once"
- [o] Proper debug level control
- [o] Use StorageAdapter from vendor "lst" also at "hiveeyes"
- [o] Use ThreadPool for storage operations
- [o] Deprecate InfluxDB 0.8 compatibility
- [o] MQTT broker connection resiliency
- [o] Start mqttkit, then mention in README.rst at "For developers"
- [o] Improve application bootstrapping by refactoring into a Twisted plugin
- [o] REST API
- [o] Throttle metrics output to one per minute after 90 seconds
- [o] Assure communication between Kotori and InfluxDB is efficient (UDP, anyone?)
- [o] Mechanisms for resetting database and dashboard
- [o] LST: Headerfile upload API and browser drop target
- [o] GUI: Interactively create data sinks, add decoding- and mapping-rules and ...
- [o] Start dogfeeding by collecting data from Kotori's builtin metrics subsystem
- [o] README: Add foreword about contemporary space ship design and afterword about
      testing, feedback, contributions and more use cases
- [o] Documentation content license: Creative commons share-alike attribution non-commercial
- [o] Documentation content attributions

    - Kotori Logo: Google Material Design Icons
    - Hexagon Buttons: https://github.com/shariarbd/CSS3-Hexagon-Buttons
    - Entypo Font: http://www.entypo.com/ (Entypo pictograms by Daniel Bruce — http://entypo.com/)
    - https://github.com/mqtt/mqttorg-graphics
    - InfluxDB logo: http://svgporn.com/


2016-03-25
==========
- Use the PiDrive

    - http://wdlabs.wd.com/
    - http://arstechnica.co.uk/gadgets/2016/03/wd-314gb-raspberry-pi-pidrive/

- Blueprint for creating images

    - https://owncloud.org/blog/wd-labs-raspberry-pi-owncloud-and-ubuntu/
    - https://github.com/owncloud/pi-image/tree/master/image-creation-tools



2016-03-23
==========
- | Integrate with Plottico
  | Live plotting that just works.
  | http://plotti.co/
  | https://news.ycombinator.com/item?id=11290122

- Write about EDU_HM_LST_ORC

- | Kotori Box XT
  | http://www.pollin.de/shop/dt/MTY1OTgxOTk-/Bausaetze_Module/Entwicklerboards/Odroid/ODROID_XU4_Set_mit_8GB_eMMC_Modul_Gehaeuse_und_Netzteil.html


2016-03-20
==========
- [o] Receive telemetry data via Ice-E: https://zeroc.com/products/ice-e


2016-03-17
==========
- Integrate with other Home Automation Systems

    - http://www.domoticz.com/DomoticzManual.pdf

- Integrate with Z-Wave

    - http://razberry.z-wave.me/
    - http://razberry.z-wave.me/index.php?id=9
    - http://razberry.z-wave.me/index.php?id=6
    - http://razberry.z-wave.me/index.php?id=10
    - http://razberry.z-wave.me/index.php?id=4
    - http://www.zwave4u.com/index.php?cat=153&sort=&XTCsid=3a0993c6f56070cb8bf68d4e2e0a900b&filter_id=38
    - http://www.zwave4u.com/PC-Adapters/-USB-Sticks/USB-Stick-incl-Z-Way-Controller-Software-ZMEEUZBWAY::17762.html
    - http://ser2net.sourceforge.net/


2016-03-15
==========
- [o] Integrate with *Phywe* datalogging system *Cobra3*/*Cobra4*

    - https://www.phywe.com/en/geraetehierarchie/datalogging-system-cobra4/
    - | Cobra4 - The Universal Measurement System for Scientific Instruction
      | https://www.youtube.com/watch?v=1rt6wdMbQYA
    - https://www.phywe.com/en/software-measure-cobra3.html
    - https://www.phywe.com/en/cobra3-basic-unit-set.html
    - https://www.phywe.com/en/top/downloads/softwaredownload/
    - https://www.phywe.com/en/software-cobra4-multi-user-licence.html
    - http://repository.phywe.de/files/bedanl.pdf/14550.61/e/1455061e.pdf
    - http://www.phywe-es.com/1054n531/Servicios/Descargas/Software.htm
    - https://appdb.winehq.org/objectManager.php?sClass=application&iId=11332
    - https://appdb.winehq.org/appimage.php?iId=29368


2016-03-08
==========
- [o] Make Kotori handle Gigabytes of data
- [o] Universal radio-based sensor node with appropriate housing and battery power supply, per :ref:`vendor-hiveeyes`
- [o] GPS beacon node visualizing movement on a realtime map, per prototype of :ref:`vendor-hydro2motion`,
      maybe as panel for Grafana. Maybe run mapserver on box for offline maps.

    - http://www.dfrobot.com/index.php?route=product/product&product_id=481&search=dfrduino+gps&am

- [o] Hook "Kotori Box" into DNS using VPN tunnel, for convenient remote access. Also think about remote-hands maintenance.


2016-03-07
==========
- [o] Use NodeUSB_ as Lua development platform and sensor network gateway adapter for WiFi devices
- [o] Integrate with the OpenXC_ platform using `OpenXC for Python`_
- [o] Integrate with other cloud IoT platforms as up- or downstream unit
- [o] Use the `Funky v3`_ as canonical sensor node?


2016-03-06
==========
- [o] "Kotori Box" demo setup on Raspberry Pi 3
- [o] Improve docs

    - redesign page for ilaundry applications
    - short history sections for all applications
    - content policy / ownership


2016-02-20
==========

Milestone 1 - Kotori 0.6.0
--------------------------
- [x] Arbeit an der Dokumentation, siehe commits von gestern
- [x] Vorbereitung des Release 0.6.0 im aktuellen Zustand mit den Doku Updates (die 0.5.1 ist vom 26. November)
- [o] Release eines einigermaßen sauberen bzw. benutzbaren Debian Pakets


Milestone 2 - Kotori 0.7.0
--------------------------
- [x] Reguläres refactoring
- [o] MQTT Topic

    - [o] Implementierung der "Content Type" Signalisierung über pseudo-Dateiendungen wie geplant
      (Inspired by Nick O’Leary and Jan-Piet Mens; Acked by Clemens and Richard)::

            hiveeyes/testdrive/area42/hive3/temperature vs. hiveeyes/testdrive/area42/hive3.json

    - [o] Weitere Diskussion und Implementierung der "Direction" Signalisierung (Inspired by computourist, Pushed by Richard)
      Proposal: ``.../node3/{direction}/{sensor}.foo``

- [x] Generalisierung der BERadioNetworkApplication / HiveeyesApplication vendor Architektur
- [o] Verbesserung der service-in-service Infrastruktur mit nativen Twisted service containern
- [o] Flexiblere Anwendungsfälle ähnlich dem von Hiveeyes ermöglichen: mqtt topic first-level segment "hiveeyes/"
      (the "realm") per Konfigurationsdatei bestimmen (Wunsch von Dazz)
- [o] Einführung von Softwaretests


Hiveeyes Research
-----------------
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


2016-01-25
==========
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
==========
- [o] Grafana Manager: Create dashboard row per gateway in same network
- [o] MQTT signals on thresholds
- [o] Add email alerts on tresholds
- [o] When sending whole bunches of measurements, ignore fields having leading underscores for Grafana panel creation
- [o] The order of the Grafana panels (temperature, humidity, weight) works in Grafana 2.1.3, but not in Grafana 2.6.0


2016-01-27 A
============
- [x] systemd init script
- [o] Send measurements by HTTP POST and UDP, republish to MQTT
- [o] Mechanism / button to reset the "testdrive" database (or any other?).
      This is required when changing scalar types (e.g. str -> float64, etc.)

2016-01-27 B
============
- [o] Numbers and gauges about message throughput
- [o] systemd init script for crossbar

2016-01-28 A
============
- [x] Get rid of the [vendor] configuration settings, use instead::

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
============
- [o] Improve error message if MQTT daemon isn't listening - currently::

    2016-01-28T21:52:13+0100 [mqtt.client.factory.MQTTFactory  ] INFO: Starting factory <mqtt.client.factory.MQTTFactory instance at 0x7f5105e157a0>
    2016-01-28T21:52:13+0100 [mqtt.client.factory.MQTTFactory  ] INFO: Stopping factory <mqtt.client.factory.MQTTFactory instance at 0x7f5105e157a0>


2016-01-29
==========
- [o] Switch to PAHO
    - https://pypi.python.org/pypi/paho-mqtt/
    - https://www.eclipse.org/paho/clients/python/
    - https://git.eclipse.org/c/paho/org.eclipse.paho.mqtt.python.git/tree/src/paho/mqtt/client.py


----


****
2015
****

LST
===

Prio 1 - Showstoppers
====================-

Besides making it work in approx. 30 min. on the first hand (cheers!), there are some remaining issues making the wash&go usage
of Kotori somehow inconvenient in day-to-day business. Let's fix them.

- Currently nothing on stack.


Prio 1.5 - Important
====================
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
    2015-11-20T16:56:57+0100 [kotori.daq.storage.influx        ] ERROR: Unable to format event {'log_namespace': 'kotori.daq.storage.influx', 'log_level': <LogLevel=error>, 'log_logger': <Logger 'kotori.daq.storage.influx'>, 'log_time': 1448035017.722721, 'log_source': None, 'log_format': 'Processing Bus message failed: 401: {"error":"user not found"}\nERROR: InfluxDBClientError: 401: {{"error":"user not found"}}\n\n============================================================\nEntry point:\nFilename:    /home/basti/kotori/kotori/daq/storage/influx.py\nLine number: 171\nFunction:    bus_receive\nCode:        return self.process_message(self.topic, payload)\n============================================================\nSource of exception:\nFilename:    /home/basti/kotori/.venv27/local/lib/python2.7/site-packages/influxdb-2.9.2-py2.7.egg/influxdb/client.py\nLine number: 247\nFunction:    request\nCode:        raise InfluxDBClientError(response.content, response.status_code)\n\nTraceback (most recent call last):\n  File "/home/basti/kotori/kotori/daq/storage/influx.py", line 171, in bus_receive\n    return self.process_message(self.topic, payload)\n  File "/home/basti/kotori/kotori/daq/storage/influx.py", line 195, in process_message\n    self.store_mes

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
==========-
- dynamic receiver channels
- realtime scope views: embed grafana Graphs or render directly e.g. using Rickshaw.js?

    - http://docs.grafana.org/v2.0/reference/sharing/
    - https://github.com/grafana/grafana/issues/1622
    - https://github.com/ricklupton/livefft

Milestone 2
==========-
- pdf renderer
- derivation and integration
