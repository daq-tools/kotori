.. include:: ../../_resources.rst

.. highlight:: bash

.. _data-export:
.. _export-handbook:

###########
Data export
###########

********
Synopsis
********
Exporting data to CSV_, HTML_ or XLSX_ (Excel) is just a matter of accessing the appropriate HTTP endpoint::

    http://localhost:24642/api/mqttkit-1/testdrive/area-42/node-1/data.csv
    http://localhost:24642/api/mqttkit-1/testdrive/area-42/node-1/data.html
    http://localhost:24642/api/mqttkit-1/testdrive/area-42/node-1/data.xlsx

.. note:: The suffix (``.txt``, ``.html``, ``.xlsx``) controls the output format.


************
Introduction
************
Kotori offers a HTTP interface for exporting timeseries data to various
tabular and hierarchical data formats and different timeseries plots.
After querying InfluxDB, data is channeled through a pandas_ DataFrame_
object and routed to a flexible rendering machinery, which supports a
number of output formats out of the box:

.. container:: align-left padding-right-regular

    Tabular data

    - CSV_
    - JSON_
    - HTML_
    - XLSX_
    - DataTables_

.. container:: align-left padding-right-regular

    Hierarchical data

    - HDF5_
    - NetCDF_

.. container:: align-left

    Timeseries plots

    - matplotlib_
    - ggplot_
    - dygraphs_
    - Bokeh_
    - Vega_, using Vincent_

|clearfix|


*******
Details
*******

Setup
=====
To make Kotori listen to HTTP requests for raw data export and data plot
rendering, please have a look at :ref:`forward-http-to-influx` about how to
configure a HTTP endpoint for accessing and querying data in InfluxDB_.

List of output formats
======================
Possible suffixes are (.csv, .txt), .json, .html, .xlsx, (.hdf, .hdf5, .h5), (.nc, .cdf),
(.dy, .dygraphs), (.dt, .datatables), (.bk, .bokeh), (.vega, .vega.json), .png

.. todo:: Make table which maps extension to description/web link, maybe combine with table from Introduction

.. todo:: Add gallery of exports.

.. todo:: Mention .png?renderer=ggplot&theme=... and .png?style=...


Download
========
Download data using HTTPie_::

    export HTTP_URI=http://localhost:24642
    export MQTT_TOPIC=mqttkit-1/testdrive/area-42/node-1

    http GET $HTTP_URI/api/$MQTT_TOPIC/data.csv  --download
    http GET $HTTP_URI/api/$MQTT_TOPIC/data.xlsx --download


Date ranges
===========
Date ranges can be specified using the HTTP URI query parameters ``from`` and ``to``.
Both accept absolute and relative datetime expressions. If omitted, the defaults are
``from=now-10d`` and ``to=now``.

Absolute timestamps:

- ?from=2016-06-25T22:00:00.000Z
- ?from=2016-06-26T00:00:00.000%2B02:00    (%2B is "+" urlencoded)
- ?from=2016-06-25
- ?from=20160625

Relative datetime expressions:

- ?from=now-4h&to=now-2h
- ?from=now-8d5h3m&to=now-6d

.. attention::

    Please recognize absolute datetimes are expected to be in ISO 8601 format.
    Default is UTC, optionally specify an appropriate timezone offset. There's
    another, ISO 8601-like convenience format without separators.
    The accepted datetime formats are::

        YYYY-MM-DDTHH:mm:ss.%sZ
        YYYY-MM-DD
        YYYYMMDDTHHmmssZ
        YYYYMMDD

    When a straight date without time component is supplied as value to the ``to``
    parameter (e.g. YYYY-MM-DD or YYYYMMDD), the date is ceiled to YYYY-MM-DDT23:59:59.999,
    which is most probably what you want anyway (DWIM_).

Examples using HTTPie_::

    http GET $HTTP_URI/api/$MQTT_TOPIC/data.csv from=now-30m
    http GET $HTTP_URI/api/$MQTT_TOPIC/data.csv from=now-2h
    http GET $HTTP_URI/api/$MQTT_TOPIC/data.csv from=now-1h to=now-20m
    http GET $HTTP_URI/api/$MQTT_TOPIC/data.csv from=2016-06-26T12:42:59.000+02:00
    http GET $HTTP_URI/api/$MQTT_TOPIC/data.csv from=20160626T124259+0200
    http GET $HTTP_URI/api/$MQTT_TOPIC/data.csv from=20160626T124259Z to=20160628T124259Z


Hierarchical data
=================
Kotori supports exporting data in HDF5_ and NetCDF_ formats.
See :ref:`export-hierarchical-data`.

