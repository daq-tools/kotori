.. include:: ../_resources.rst

.. _database-influxdb:

########
InfluxDB
########


*****
About
*****

`InfluxDB`_ is a scalable datastore and time series platform for metrics, events,
and real-time analytics. It covers storing and querying data, background ETL processing
for monitoring and alerting purposes, and visualization and exploration features.


*******
Details
*******

This section summarizes InfluxDB's data model and query interface.

Data model
==========

InfluxDB stores data points (records) in measurements. Measurements are analogous to
tables in relational databases. Measurements have been grouped into databases within
InfluxDB 1.x, while those have been repurposed to "buckets" with InfluxDB 2.x.

Each data point within a measurement has a timestamp, fields, and tags.

.. figure:: https://github.com/daq-tools/kotori/assets/453543/6f9c00bb-d834-4adf-b752-a069c48f7b56
    :target: https://invidious.fdn.fr/watch?v=1Iw_0J5UkYs&t=257
    :width: 400
    :alt: An InfluxDB data point by example.

On disk, timestamps are stored in epoch nanosecond format. InfluxDB formats timestamps
in RFC3339 UTC.

Tags are indexed, and store low-cardinality metadata, for example location information
about the data point. Fields are not indexed, and store the actual measurement values
of the data point.

Not sure what to store in tags and what to store in fields?

- Store commonly-queried and grouping (``group()`` or ``GROUP BY``) metadata in tags.
- Store data in fields if each data point contains a different value.
- Store numeric values as fields (tag values only support string values).

Query interface
===============

Languages
---------
InfluxDB 1.x supports both the `Influx Query Language (InfluxQL)`_ and the `Flux data
scripting language`_ for querying data, and the `InfluxDB line protocol`_ for inserting
data. Please inspect the :ref:`influxdb-query-examples`, as well as the corresponding
upstream documentation about how to `insert data`_, `query data using InfluxQL`_, and
`query data using Flux`_.

Protocols
---------
InfluxDB clients communicate to servers using HTTP or UDP.


************
Key features
************

This section enumerates the key features of InfluxDB, as advertised on its documentation.

Storage engine
==============

The `InfluxDB storage engine`_ includes the following components.

- **Write Ahead Log (WAL)**

  The Write Ahead Log (WAL) retains InfluxDB data when the storage engine restarts.
  The WAL ensures data is durable in case of an unexpected failure.

- **Cache**

  The cache is an in-memory copy of data points currently stored in the WAL. The WAL
  and cache are separate entities and do not interact with each other. The storage
  engine coordinates writes to both.

- **Time-Structured Merge Tree (TSM)**

  To efficiently compact and store data, the storage engine groups field values by series
  key, and then orders those field values by time. The storage engine uses a Time-Structured
  Merge Tree (TSM) data format. TSM files store compressed series data in a columnar format.
  To improve efficiency, the storage engine only stores differences (or deltas) between
  values in a series. Column-oriented storage lets the engine read by series key and omit
  extraneous data.

- **Time Series Index (TSI)**

  As data cardinality (the number of series) grows, queries read more series keys and become
  slower. The Time Series Index ensures queries remain fast as data cardinality grows. The
  TSI stores series keys grouped by measurement, tag, and field, and allows the database to
  answer metadata queries about what measurements, tags, or fields exist, and, given a
  measurement, tags, and fields, what series keys exist.

Query API
=========

- RESTful API and a set of client libraries (InfluxDB API, Arduino, C#, Go, Java,
  JavaScript, Kotlin, Node.js, PHP, Python, R, Ruby, Scala, and Swift) to collect,
  transform, and visualize your data.

- The Flux query language is a functional language for working with time series data.

Ecosystem
=========

InfluxDB is supported by a massive community and ecosystem, offering a wide
range of connectivity options.

- Telegraf is an open source collector agent with over 300+ plugins.
- Write data with AWS Lambda or InfluxDB CL.
- Run Flux scripts natively and show results in VS Code.
- Use the Flux REPL (Read–Eval–Print Loop) to execute Flux scripts.
- Use the Flux language to interact with InfluxDB and other data sources.
- Connectors to Grafana, Google Data Studio, and PTC ThingWorx.
- Use Postman to interact with the InfluxDB API.

User interface
==============

A best-in-class UI that includes a data explorer, dashboarding tools, and a script editor.

- Quickly browse through stored metric and event data.
- Apply common transformations.
- The dashboarding tool includes a number of visualizations that help you to see insights
  from your data faster.
- The script editor offers easily accessible examples, in order to quickly learn the Flux
  query language, and features auto-completion and real-time syntax checking.


.. _influxdb-query-examples:

**************
Query examples
**************

This section demonstrates a few basic query examples from InfluxDB's documentation.

Insert
======

Data is inserted into InfluxDB using the `InfluxDB line protocol`_, without using a
query language.

Select
======
.. code-block:: sql

    -- InfluxQL: Basic select statement with date range filtering.
    SELECT "water_level"
    FROM "h2o_feet"
    WHERE
        "location"='coyote_creek' AND
        time >= '2015-08-18T00:00:00Z' AND
        time <= '2015-08-18T00:18:00Z'

.. code-block:: cpp

    // Flux: Select most recent reading from a measurement, with date range filtering.
    from(bucket:"turbines")
      |> range(start: -1h)
      |> filter(fn: (r) => r._measurement == "turbine3000")
      |> last()

Advanced queries
================

.. code-block:: sql

    -- InfluxQL: Aggregations with date range filtering and
    --           time bucketing using specified intervals.
    SELECT mean("humidity")
    FROM "readings"
    WHERE time > now()-1h
    GROUP BY time(5m)

.. code-block:: cpp

    // Flux: Group records using regular time intervals.
    // Window every 20 seconds covering 40 second periods.
    data
        |> window(every: 20s, period: 40s)

.. code-block:: cpp

    // Flux: Time bucketing.
    // Apply downsampling by grouping data into fixed windows of time and applying an
    // aggregate or selector function to each window.
    data
        |> aggregateWindow(every: 1mo, fn: mean)

.. code-block:: cpp

    // Flux: Time bucketing with parameterized aggregation function.
    data
        |> aggregateWindow(
            column: "_value",
            every: 20s,
            fn: (column, tables=<-) => tables |> quantile(q: 0.99, column: column),
        )


*****
Usage
*****

Purpose
=======

Kotori uses InfluxDB to store **timeseries-data** of data acquisition channels.

Documentation
=============

See :ref:`influxdb-handbook` and the `InfluxDB OSS documentation`_.

Compatibility
=============

Kotori supports data acquisition and export with InfluxDB 1.x.

.. todo:: It is not compatible with InfluxDB 2.x and 3.x.


.. _insert data: https://docs.influxdata.com/influxdb/v1.8/write_protocols/line_protocol_tutorial/#writing-data-to-influxdb
.. _query data using InfluxQL: https://docs.influxdata.com/influxdb/v1.8/query_language/sample-data/#test-queries
.. _query data using Flux: https://docs.influxdata.com/influxdb/v1.8/flux/guides/execute-queries/
