.. include:: ../_resources.rst

.. _database-cratedb:

#######
CrateDB
#######


*****
About
*****

`CrateDB`_ is a distributed and scalable SQL database for storing and analyzing massive
amounts of data in near real-time, even with complex queries. It is PostgreSQL-compatible,
and based on `Lucene`_.


*******
Details
*******

This section summarizes CrateDB's data model and query interface.

Data model
==========

As a time-series/document/OLAP/RDBMS database with an SQL interface, CrateDB stores records
into tables. Tables are grouped into schemas, which is equivalent to the concept of hosting
multiple databases on the same server instance.

The schema of tables/records can be freely defined using a classic SQL DDL statement,
leveraging CrateDB's multi-modal data types. The tables can be queried also by using
classic, standards-compliant SQL DQL statements.

.. figure:: https://github.com/daq-tools/kotori/assets/453543/fb469738-9d3e-4258-b546-1f5cd9bac261
    :width: 640
    :alt: A screenshot example of an SQL query submitted to CrateDB.

Other than the record-based scheme of RDBMS databases, CrateDB also allows you to store
and retrieve nested data, by providing `container types`_ ``ARRAY`` and ``OBJECT``,
effectively providing document-oriented capabilities like CouchDB or MongoDB.

On disk, CrateDB stores data into Lucene indexes. By default, all fields are indexed,
nested or not, but the indexing can be turned off selectively.

Query interface
===============

Languages
---------
CrateDB supports SQL as query language. Please inspect the :ref:`cratedb-query-examples`,
as well as the corresponding upstream documentation about how to `insert data`_ and
`query data`_.

Protocols
---------
CrateDB clients communicate to servers using either HTTP, or by using the `PostgreSQL
wire protocol`_, version 3.


************
Key features
************

This section enumerates the key features of CrateDB, as advertised on its documentation.

At a glance
===========

- Use standard SQL via the PostgreSQL wire protocol or an HTTP API.
- Dynamic table schemas and queryable objects provide document-oriented features in
  addition to the relational features of SQL.
- Support for time-series data, realtime full-text search, geospatial data types and
  search capabilities.
- Horizontally scalable, highly available and fault tolerant clusters that run very
  well in virtualized and containerised environments.
- Extremely fast distributed query execution.
- Auto-partitioning, auto-sharding, and auto-replication.
- Self-healing and auto-rebalancing.
- User-defined functions (UDFs) can be used to extend the functionality of CrateDB.

Storage layer
=============

Lucene
------

The CrateDB storage layer is based on Lucene. This section enumerates some concepts of
Lucene, and the article `Indexing and Storage in CrateDB`_ goes into more details by
exploring its internal workings.

Lucene offers scalable and high-performance indexing which enables efficient search and
aggregations over documents and rapid updates to the existing documents. Solr and
Elasticsearch are building upon the same technologies.

- **Documents**

  A single record in Lucene is called "document", which is a unit of information for search
  and indexing that contains a set of fields, where each field has a name and value. A Lucene
  index can store an arbitrary number of documents, with an arbitrary number of different fields.

- **Append-only segments**

  A Lucene index is composed of one or more sub-indexes. A sub-index is called a segment,
  it is immutable, and built from a set of documents. When new documents are added to the
  existing index, they are added to the next segment, while previous segments are never
  modified. If the number of segments becomes too large, the system may decide to merge
  some segments and discard the freed ones. This way, adding a new document does not require
  rebuilding the whole index structure completely.

- **Column store**

  For text values, other than storing the row data as-is (and indexing each value by default),
  each value term is stored into a `column-based store`_ by default, which offers performance
  improvements for global aggregations and groupings, and enables efficient ordering, because
  the data for one column is packed at one place.

  In CrateDB, the column store is enabled by default and can be disabled only for text fields,
  not for other primitive types. Furthermore, CrateDB does not support storing values for
  container and geospatial types in the column store.

Data structures
---------------

This section enumerates the three main Lucene data structures that are used within
CrateDB: Inverted indexes for text values, BKD trees for numeric values, and DocValues.

- **Inverted index**

  The Lucene indexing strategy for text fields relies on a data structure called inverted
  index, which is defined as a "data structure storing a mapping from content, such as
  words and numbers, to its location in the database file, document or set of documents".

  Depending on the configuration of a column, the index can be plain (default) or full-text.
  An index of type "plain" indexes content of one or more fields without analyzing and
  tokenizing their values into terms. To create a "full-text" index, the field value is
  first analyzed and based on the used analyzer, split into smaller units, such as
  individual words. A full-text index is then created for each text unit separately.

  The inverted index enables a very efficient search over textual data.

- **BKD tree**

  To optimize numeric range queries, Lucene uses an implementation of the Block KD (BKD)
  tree data structure. The BKD tree index structure is suitable for indexing large
  multi-dimensional point data sets. It is an I/O-efficient dynamic data structure based
  on the KD tree. Contrary to its predecessors, the BKD tree maintains its high space
  utilization and excellent query and update performance regardless of the number of
  updates performed on it.

  Numeric range queries based on BKD trees can efficiently search numerical fields,
  including fields defined as ``TIMESTAMP`` types, supporting performant date range
  queries.

- **DocValues**

  Because Lucene's inverted index data structure implementation is not optimal for
  finding field values by given document identifier, and for performing column-oriented
  retrieval of data, the DocValues data structure is used for those purposes instead.

  DocValues is a column-based data storage built at document index time. They store
  all field values that are not analyzed as strings in a compact column, making it more
  effective for sorting and aggregations.

Clustering
==========

Overview
--------

CrateDB splits tables into shards and replicas, meaning that tables are divided and
distributed across the nodes of a cluster. Each shard in CrateDB is a Lucene index
broken into segments and stored on the filesystem.

CrateDB has been designed with clustering capabilities from the very beginning. The
clustering subsystem, effectively and efficiently distributing data amongst multiple
storage nodes, is originally based on prior art technology implementations from
Elasticsearch, in turn based on both quorum-based consensus algorithms as well as
primary-backup approaches.

Benefits
--------

Database clusters are effective for storing and retrieving large amounts of data,
in the range of billions of records, and terabytes of data.

On data retrieval, CrateDB's distributed query execution engine parallelizes query
workloads across the whole cluster.

By distributing data to multiple machines, and properly configuring replication
parameters, you are also adding redundancy to your data, so it is protected against
data-loss resulting from fatal failures of individual storage nodes.

Those concepts implement similar features like RAID drives, for the purposes of data
redundancy, performance improvements, or both.

Early distributed systems and databases needed manual operations procedures, for
example to initiate node fail-over procedures. With CrateDB, the corresponding steps
around partitioning, sharding, replication, and rebalancing, are performed unattended
and automatically, effectively providing cluster self-healing capabilities.

Complex queries
===============

By using the SQL query language, CrateDB provides an advanced query execution layer,
unlocking complex querying capabilities like date range filtering, sub-selects,
aggregations, JOINs, UNIONs, and CTEs, all within the same SQL statement.

Query API
=========

- CrateDB provides an `HTTP endpoint`_ that can be used to submit SQL queries.
  As such, any HTTP client, like curl or Postman, can be used to communicate with CrateDB.

- The standards-based `PostgreSQL wire protocol`_ interface unlocks compatibility
  with a wide range of client applications which can talk to PostgreSQL servers.

Ecosystem
=========

CrateDB offers a wide range of connectivity options. In general, any PostgreSQL-
compatible driver or framework can be used to connect to CrateDB.

- `Overview of CrateDB drivers and adapters`_
- `Overview of CrateDB integration tutorials`_

User interface
==============

CrateDB offers both a graphical-, and a commandline-based user interface. In general,
any PostgreSQL-compatible applications and systems can be used to connect to CrateDB.

- CrateDB Admin, a graphical, web-based user interface, is built into CrateDB.
- ``crash`` is a command-line based terminal program, similar to ``psql``, but
  with a bit more convenience.


.. _cratedb-query-examples:

**************
Query examples
**************

This section demonstrates a few query examples from CrateDB's documentation.

Typical queries
===============

.. code-block:: sql

    -- Aggregations with date range filtering and
    -- time bucketing using specified intervals.
    SELECT
        DATE_BIN('5 min'::INTERVAL, time::TIMESTAMPTZ, 0) AS time,
        MEAN(fields['humidity']) AS humidity
    FROM
        readings
    WHERE
        time > NOW() - '1 hour'::INTERVAL
    GROUP BY
        time
    ORDER BY
        time;

.. code-block:: sql

    -- An SQL DDL statement defining a custom schema for holding sensor data.
    CREATE TABLE iot_data (
      timestamp TIMESTAMP WITH TIME ZONE,
      sensor_data OBJECT (DYNAMIC) AS (
        temperature FLOAT,
        humidity FLOAT,
        location OBJECT (DYNAMIC) AS (
          latitude DOUBLE PRECISION, longitude DOUBLE PRECISION
        )
      )
    );

.. code-block:: sql

    -- Inserting data into the table defined above.
    INSERT INTO iot_data (ts, sensor_data) VALUES
        -- Vienna
        ('2022-01-01T01:00:00', '{"temperature": 20.3, "humidity": 50.5, "location": {"latitude": 48.2082, "longitude": 16.3738}}'),
        -- Stockholm
        ('2022-01-01T02:00:00', '{"temperature": 18.0, "humidity": 55.2, "location": {"latitude": 59.3293, "longitude": 18.0686}}'),
        -- Tokyo
        ('2022-01-01T03:00:00', '{"temperature": 24.5, "humidity": 60.8, "location": {"latitude": 35.6895, "longitude": 139.6917}}'),
        -- Sydney
        ('2022-01-01T04:00:00', '{"temperature": 25.7, "humidity": 65.0, "location": {"latitude": -33.8688, "longitude": 151.2093}}');

.. code-block:: sql

    -- Create a user-defined function to calculate the distance between two coordinates.
    CREATE FUNCTION haversine_distance(
      lat1 DOUBLE PRECISION, lon1 DOUBLE PRECISION,
      lat2 DOUBLE PRECISION, lon2 DOUBLE PRECISION
    ) RETURNS DOUBLE PRECISION LANGUAGE JAVASCRIPT AS '...';

    -- Use the user-defined function with nested data.
    SELECT
      id,
      haversine_distance(
        sensor_data[ 'location' ][ 'latitude' ],
        sensor_data[ 'location' ][ 'longitude' ],
        40.7128, -74.0060
      ) AS distance
    FROM
      iot_data
    ORDER BY
      distance;


Advanced queries
================

Time-series data
----------------

.. code-block:: sql

    /**
     * Based on device data, this query returns the average
     * of the battery level for every hour for each `device_id`.
    **/

    WITH avg_metrics AS (
        SELECT device_id,
            DATE_BIN('1 hour'::INTERVAL, time, 0) AS period,
            AVG(battery_level) AS avg_battery_level
        FROM devices.readings
        GROUP BY 1, 2
        ORDER BY 1, 2
    )
    SELECT period,
        t.device_id,
        manufacturer,
        avg_battery_level
    FROM avg_metrics t, devices.info i
    WHERE t.device_id = i.device_id
        AND model = 'mustang'
    LIMIT 10;


IoT & sensor data
-----------------

.. code-block:: sql

    /**
     * Based on data acquisition from power metering devices, this query
     * returns the voltage corresponding to the maximum global active power
     * for each `meter_id`.
    **/

    SELECT meter_id,
        MAX_BY("Voltage", "Global_active_power") AS voltage_max_global_power
    FROM iot.power_consumption
    GROUP BY 1
    LIMIT 10;

Geospatial tracking
-------------------

.. code-block:: sql

    /**
     * Based on the location of the International Space Station,
     * this query returns the 10 closest capital cities from
     * the last known position.
    **/

    SELECT city AS "City Name",
        country AS "Country",
        DISTANCE(i.position, c.location)::LONG / 1000 AS "Distance [km]"
    FROM demo.iss i
    CROSS JOIN demo.world_cities c
    WHERE capital = 'primary'
        AND ts = (SELECT MAX(ts) FROM demo.iss)
    ORDER BY 3 ASC
    LIMIT 10;

Log analysis
------------

.. code-block:: sql

    /**
     * Based on system event logs, this query calculates:
     * - a filter for specific messages using a full-text index
     * - the number of entries per minute
     * - the average scoring ratio for each matched row
    **/

    SELECT DATE_TRUNC('minute', receivedat) AS event_time,
        COUNT(*) AS entries,
        AVG(_score) AS avg_score
    FROM "syslog"."systemevents"
    WHERE MATCH(message, 'authentication failure')
    USING most_fields WITH (analyzer = 'whitespace')
        AND MATCH(syslogtag, 'sshd')
    GROUP BY 1
    ORDER BY 1 DESC
    LIMIT 10;

Tracking analytics
------------------

This complex query executes in under 200 milliseconds on two tables containing
6 million records (``pageview``), respectively 35_000 records (``user_session``).

.. code-block:: sql

    /**
     * An analytics query about user visits and metrics.
     * This SQL DQL statement uses date range filtering,
     * sub-selects, aggregations, JOINs, UNIONs, and CTEs.
    **/

    WITH sessions AS (
      SELECT
        user_id,
        session_id
      FROM
        af_dev.user_session
      WHERE
        user_session.domain = 'domain.com'
        AND user_session.hostname = 'www.domain.com'
        AND user_session.event_time BETWEEN '2022-12-05' AND '2023-01-05'
        AND user_session.device_type IS NOT NULL
    ),
    pageviews AS (
      SELECT
        pageview.totaltime,
        pageview.user_id,
        pageview.event_time
      FROM
        af_dev.pageview
      WHERE
        pageview.event_time BETWEEN '2022-12-05' AND '2023-01-05'
        AND pageview.domain = 'domain.com'
        AND pageview.host = 'www.domain.com'
    ),
    visits AS (
      SELECT
        MAX(totaltime) AS sess_len,
        COUNT(session_id) AS sess_count,
        COUNT(DISTINCT sessions.user_id) AS visitors,
        MIN(event_time) AS event_time
      FROM
        pageviews
        JOIN sessions ON pageviews.user_id = sessions.user_id
      GROUP BY
        pageviews.user_id,
        sessions.session_id
    ),
    psessions AS (
      SELECT
        user_id,
        session_id
      FROM
        af_dev.user_session
      WHERE
        user_session.domain = 'domain.com'
        AND user_session.hostname = 'www.domain.com'
        AND user_session.event_time BETWEEN '2022-11-05' AND '2022-12-05'
        AND user_session.device_type IS NOT NULL
    ),
    ppageviews AS (
      SELECT
        pageview.totaltime,
        pageview.user_id,
        pageview.event_time
      FROM
        af_dev.pageview
      WHERE
        pageview.event_time BETWEEN '2022-11-05' AND '2022-12-05'
        AND pageview.domain = 'domain.com'
        AND pageview.host = 'www.domain.com'
    ),
    pvisits AS (
      SELECT
        MAX(totaltime) AS sess_len,
        COUNT(session_id) AS sess_count,
        COUNT(DISTINCT psessions.user_id) AS visitors,
        MIN(event_time) AS event_time
      FROM
        ppageviews
        JOIN psessions ON ppageviews.user_id = psessions.user_id
      GROUP BY
        ppageviews.user_id,
        psessions.session_id
    )
    SELECT
          MIN(event_time) AS event_date,
          SUM(visitors) AS tot_vis,
          SUM(visitors) FILTER (WHERE sess_count = 1) AS new_vis,
          SUM(visitors) FILTER (WHERE sess_count > 1) AS ret_vis,
          AVG(sess_len) AS tot_avg,
          AVG(sess_len) FILTER (WHERE sess_count = 1) AS new_avg,
          AVG(sess_len) FILTER (WHERE sess_count > 1) AS ret_avg
    FROM visits
    UNION
    SELECT
          MIN(event_time) AS event_date,
          SUM(visitors) AS tot_vis,
          SUM(visitors) FILTER (WHERE sess_count = 1) AS new_vis,
          SUM(visitors) FILTER (WHERE sess_count > 1) AS ret_vis,
          AVG(sess_len) AS tot_avg,
          AVG(sess_len) FILTER (WHERE sess_count = 1) AS new_avg,
          AVG(sess_len) FILTER (WHERE sess_count > 1) AS ret_avg
    FROM pvisits;


*****
Usage
*****

Purpose
=======

Kotori uses CrateDB to store **timeseries-data** of data acquisition channels.

Documentation
=============

See :ref:`cratedb-handbook` and the `CrateDB reference documentation`_.

Compatibility
=============

Kotori supports data acquisition and export with CrateDB 4.2 and higher.

.. _column-based store: https://crate.io/docs/crate/reference/en/latest/general/ddl/storage.html
.. _container types: https://crate.io/docs/crate/reference/en/latest/general/ddl/data-types.html#container-types
.. _HTTP endpoint: https://crate.io/docs/crate/reference/en/latest/interfaces/http.html
.. _Indexing and Storage in CrateDB: https://crate.io/blog/indexing-and-storage-in-cratedb
.. _insert data: https://crate.io/docs/crate/reference/en/latest/general/dml.html#inserting-data
.. _Overview of CrateDB drivers and adapters: https://community.crate.io/t/overview-of-cratedb-drivers-and-adapters/1464
.. _Overview of CrateDB integration tutorials: https://community.crate.io/t/overview-of-cratedb-integration-tutorials/1015
.. _query data: https://crate.io/docs/crate/reference/en/latest/general/dql/
