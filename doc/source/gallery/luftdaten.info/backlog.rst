.. _luftdaten.info-todo:

#########################
Luftdatenpumpe v0 Backlog
#########################

- Link/embed to dashboard by Sensor ID.
- Check for proper timezone when importing CSV vs. fetching data from live API
- Filter out fields like sensor_id, location, lat, lon from timeseries data
- Convert lat/lon or latitude/longitude to geohash (The Grafana Worldmap Panel requires GeoHash)
  https://pypi.python.org/pypi/Geohash/
- Live data convergence by polling on https://api.luftdaten.info/static/v1/data.json,
  see also https://github.com/opendata-stuttgart/sensors-software/issues/33
- Resolve geohash to regional/city name
- Migrate new routines from (luftdaten.info) ``luftdatenpumpe.py`` into Kotori
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
    - ``https://luftdaten.getkotori.org/api/luftdaten/info/earth/42/data.globe?magnitudes=P1,P25,temperature&from=2017-01-01``

- Generische Tag => Filter Umsetzung à la Grafana

    - ``https://luftdaten.getkotori.org/api/luftdaten/info/earth/42/data.txt?{tagA}={valueA}&{tagB}={valueB}``
