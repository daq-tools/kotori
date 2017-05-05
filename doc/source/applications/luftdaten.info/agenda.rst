######
Agenda
######

.. contents::
   :local:
   :depth: 1

----


************
Introduction
************
- http://luftdaten.info/
- http://deutschland.maps.luftdaten.info/


*****
Goals
*****
- https://grafana.com/plugins/grafana-worldmap-panel


***********
Walkthrough
***********

Import CSV data
===============
::

    cd ~/dev/foss/contrib/luftdaten.info/archive.luftdaten.info/2017-02-25

    cat 2017-02-25_sds011_sensor_777.csv | http POST http://luftdaten.getkotori.org/api/luftdaten/testdrive/earth/42/data Content-Type:text/csv --timeout 500

    HTTP/1.1 200 OK
    Channel-Id: /mqttkit-1/testdrive/earth/42
    Content-Type: application/json
    Date: Tue, 28 Mar 2017 22:56:52 GMT
    Server: TwistedWeb/17.1.0
    Transfer-Encoding: chunked

    [
        {
            "message": "Received header fields ['sensor_id', 'sensor_type', 'location', 'lat', 'lon', 'time', 'P1', 'durP1', 'ratioP1', 'P2', 'durP2', 'ratioP2']",
            "type": "info"
        },
        {
            "message": "Received #22 readings",
            "type": "info"
        }
    ]

We added `commit 49256945 <https://github.com/zerotired/kotori/commit/49256945>`_
to make Kotori conveniently grok the CSV format used by http://archive.luftdaten.info/::

    # Convenience hack to support import from http://archive.luftdaten.info/
    elif first_line.startswith('sensor_id'):
        header_line = first_line
        data_lines.pop(0)


Grafana Worldmap Plugin
=======================

Setup
-----
https://grafana.com/plugins/grafana-worldmap-panel/installation


References
----------
- https://github.com/grafana/worldmap-panel/issues/9#issuecomment-224861471
- https://github.com/grafana/worldmap-panel/pull/20
- https://github.com/grafana/worldmap-panel/issues/30
- https://stackoverflow.com/questions/38213098/grafana-worldmap-panel-with-influxdb
- https://stackoverflow.com/questions/39154884/grafana-worldmap-panel-with-influxdb-doesnt-show-points



Vendor configuration
====================

https://github.com/zerotired/kotori/blob/master/etc/examples/vendors/luftdaten.ini

Add vendor configuration to Kotori::

    # Activate
    root@elbanco:/etc/kotori/apps-enabled# ln -s ../apps-available/luftdaten.ini .

    # Bounce daemon
    systemctl restart kotori


*****
Ready
*****

Phase 1
=======

Import CSV data (see above).

[29.03.17 02:18:04] Andreas Motl: ready: https://luftdaten.getkotori.org/

[29.03.17 02:22:08] Andreas Motl: Voilà:

    - https://luftdaten.getkotori.org/grafana/dashboard/db/luftdaten-info-automatic
    - https://luftdaten.getkotori.org/api/luftdaten/info/earth/42/data.txt?from=2017-01-01


Phase 2
=======
Feed data from live data API https://api.luftdaten.info/static/v1/data.json to MQTT using
`api_to_mqtt.py <https://github.com/zerotired/kotori/blob/master/kotori/vendor/luftdaten/api_to_mqtt.py>`_.

[29.03.17 16:44:09] Richard Pobering: ping. ich habe das dashboard jetzt inhaltlich nochmal ein bisschen angepasst:

    - https://luftdaten.getkotori.org/grafana/dashboard/db/luftdaten-testdrive-automatic

.. _luftdaten.info-todo:

****
Todo
****
- Link/embed to dashboard by Sensor ID.
- Check for proper timezone when importing CSV vs. fetching data from live API
- Filter out fields like sensor_id, location, lat, lon from timeseries data
- Convert lat/lon or latitude/longitude to geohash (The Grafana Worldmap Panel requires GeoHash)
  https://pypi.python.org/pypi/Geohash/
- Live data convergence by polling on https://api.luftdaten.info/static/v1/data.json,
  see also https://github.com/opendata-stuttgart/sensors-software/issues/33
- Resolve geohash to regional/city name
- Migrate new routines from (luftdaten.info) api_to_mqtt.py into Kotori
- Kotori: Re-create database when ERROR: Error processing MQTT message from topic "luftdaten/testdrive/earth/42/data.json": [Failure instance: Traceback: <class 'influxdb.exceptions.InfluxDBClientError'>: 404: {"error":"database not found: \"luftdaten_testdrive\""}
- Worldmap Plugin:

    - Interpolate multiple metric values into popover
    - Add HTML links to popover
    - Embed HTML into popover for generic panel generation

- Single announcement of non-volatile values to be persisted into MongoDB. Use case: Einmalig Standort registrieren.
- Generic tag announcements through field name annotations. Proposals:

    1. Send CSV header like this: ``sensor_id[@tag];sensor_type[@tag];location[@tag];lat;lon;timestamp;P1;durP1;ratioP1;P2;durP2;ratioP2``
    2. Send qualification information "out of band": ``## @tags:sensor_id,sensor_type,location``

    => Think about how to do it with JSON?::

        Why not just "@tag:sensor_id", ...?
        {temperatute: 42.42, tags: {'standort': 'Niederrhein'}}
        {tags: {'standort': 'Niederrhein'}}
        {temperatute: 42.42}

- Integrate web-gl globe:

    - https://github.com/dataarts/webgl-globe
    - https://luftdaten.getkotori.org/api/luftdaten/info/earth/42/data.globe?magnitudes=P1,P25,temperature&from=2017-01-01

- Generische tag => filter umsetzung à la Grafana

    - https://luftdaten.getkotori.org/api/luftdaten/info/earth/42/data.txt?{tagA}={valueA}&{tagB}={valueB}

