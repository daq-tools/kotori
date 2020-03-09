================
Storage adapters
================

Kotori currently lacks configuration files for its database adapters.
Please configure database access in the corresponding python files.

.. attention::

    This document is just a stub. Read the source, luke.


SQL
===

Configuration
-------------
For configuration, see kotori.node.database.sql

Query database
--------------
::

    $ sqlite3 /tmp/kotori.sqlite
    sqlite> select * from telemetry;


MongoDB
=======

Installation via MacPorts
-------------------------
Setup::

    sudo port install mongodb

Run::

    mkdir -p ./var/lib/mongodb
    mongod --dbpath=./var/lib/mongodb/


Configuration
-------------
For configuration, see kotori.node.database.mongo

Query database
--------------
::

    $ mongo kotori
    > db.telemetry.find()

