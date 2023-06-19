.. include:: ../_resources.rst

.. _database-mongodb:

#######
MongoDB
#######


*****
About
*****

`MongoDB`_ is a document database designed for ease of application development and scaling.


*******
Details
*******

This section summarizes MongoDB's data model and query interface.

Data model
==========

MongoDB stores documents in collections. Collections are analogous to tables
in relational databases. In addition to collections, MongoDB supports read-only
views and on-demand materialized views.

A record in MongoDB is a document, which is a data structure composed of field
and value pairs. MongoDB documents are similar to JSON objects. The values of
fields may include other documents, arrays, and arrays of documents.

.. figure:: https://www.mongodb.com/docs/manual/images/crud-annotated-document.bakedsvg.svg

Query interface
===============

Languages
---------
MongoDB uses the V8 JavaScript Engine to provide a query language based on ECMAscript 5,
which can be used for both inserting and querying data. Please inspect the
:ref:`mongodb-query-examples`, as well as the corresponding upstream documentation about
`MongoDB CRUD operations`_, and about how to `insert documents`_ and `query documents`_.

Protocols
---------
MongoDB clients communicate to servers using TCP and the `MongoDB Wire Protocol`_.


************
Key features
************

This section enumerates the key features of MongoDB, as advertised on its documentation.

Storage engine
==============

MongoDB provides a pluggable storage engine API, that allows third parties to develop
storage engines for MongoDB. It includes the `WiredTiger`_ and an in-memory storage
engine out of the box.

- WiredTiger is a production quality, high performance, scalable, NoSQL, Open Source
  extensible platform for data management. WiredTiger is developed and maintained by
  MongoDB, Inc., where it is the principle storage engine in the MongoDB database.

- It can be used as a simple key/value store, but also has a complete schema
  layer, including indices and projections.

- WiredTiger supports both row-oriented storage (where all columns of a row are stored
  together), and column-oriented storage (where columns are stored in groups, allowing
  for more efficient access and storage of column subsets).

- It includes ACID transactions with standard isolation levels and durability
  at both checkpoint and commit-level granularity.

- The WiredTiger storage engine supports encryption at rest.


Query API
=========

The MongoDB query API supports:

- Read and write operations (CRUD)
- Data aggregation
- Text search
- Geospatial queries

Ecosystem
=========

MongoDB offers adapters and integrations for a range of applications, frameworks,
and libraries, for data modeling, application development, monitoring, and
deployment purposes. For more information, see `MongoDB integrations`_.

High performance
================

- Embedded data models reduce I/O activity on database system.
- Indexes on document fields can include keys from embedded documents and arrays,
  supporting indexing of nested data structures.

High availability
=================

MongoDB's replication facility, called replica set, provides automatic failover
and data redundancy. A replica set is a group of MongoDB servers that maintain
the same data set, providing redundancy and increasing data availability.

Horizontal scalability
======================

- MongoDB uses sharding to distribute data across a cluster of multiple machines,
  in order to support deployments with very large data sets and high throughput
  operations.
- In sharded MongoDB clusters, you can create zones of sharded data based on the
  shard key. You can associate each zone with one or more shards in the cluster.
  A shard can associate with any number of zones. In a balanced cluster, MongoDB
  migrates chunks covered by a zone only to those shards associated with the zone,
  and directs reads and writes covered by a zone only to those shards inside the
  zone.


.. _mongodb-query-examples:

**************
Query examples
**************

.. highlight:: javascript

This section demonstrates a few basic query examples from MongoDB's documentation.

Insert
======
::

    // Insert single document into collection.
    db.inventory.insertOne(
       { item: "canvas", qty: 100, tags: ["cotton"], size: { h: 28, w: 35.5, uom: "cm" } }
    )

::

    // Insert multiple documents into collection.
    db.inventory.insertMany([
       { item: "journal", qty: 25, tags: ["blank", "red"], size: { h: 14, w: 21, uom: "cm" } },
       { item: "mat", qty: 85, tags: ["gray"], size: { h: 27.9, w: 35.5, uom: "cm" } },
       { item: "mousepad", qty: 25, tags: ["gel", "blue"], size: { h: 19, w: 22.85, uom: "cm" } }
    ])

Select
======
::

    // Query collection for all documents.
    db.inventory.find( { } )

::

    // Query collection for documents matching expression.
    db.inventory.find( { item: "canvas" } )

Advanced queries
================
::

    // Full-text search.
    // With term exclusion and ranking.
    db.stores.find(
       { $text: { $search: "java shop -coffee" } },
       { score: { $meta: "textScore" } }
    ).sort( { score: { $meta: "textScore" } } )


::

    // Geospatial search.
    // Locating objects within a specified distance, sorted from nearest to farthest.
    db.restaurants.find({ location:
        { $nearSphere: { $geometry:
            { type: "Point", coordinates: [ -73.93414657, 40.82302903 ] }, $maxDistance: 5000 } } })

::

    // Aggregation.
    // The following aggregation pipeline example contains two stages and returns
    // the total order quantity of medium size pizzas grouped by pizza name.
    db.orders.aggregate( [

        // Stage 1: Filter pizza order documents by pizza size
        {
            $match: { size: "medium" }
        },

        // Stage 2: Group remaining documents by pizza name and calculate total quantity
        {
            $group: { _id: "$name", totalQuantity: { $sum: "$quantity" } }
        }

    ] )


*****
Usage
*****

Purpose
=======

Kotori uses MongoDB to store **metadata** associated with data acquisition channels.

Documentation
=============

.. todo:: Write basic guidelines about usage and sandbox operations.

.. seealso:: In the meanwhile, please refer to the `MongoDB manual`_.

Compatibility
=============

Kotori has been tested with MongoDB 3, 4, and 5.

.. todo:: Support for MongoDB 6 and 7 has not been validated yet.


.. _insert documents: https://www.mongodb.com/docs/manual/tutorial/insert-documents/
.. _MongoDB CRUD operations: https://www.mongodb.com/docs/manual/crud/
.. _MongoDB integrations: https://cloud.mongodb.com/ecosystem/integrations
.. _query documents: https://www.mongodb.com/docs/manual/tutorial/query-documents/
