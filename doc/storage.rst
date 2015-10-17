=======================
Kotori storage adapters
=======================

Kotori currently lacks configuration files for its database adapters.
Please configure database access in the corresponding python files.

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


InfluxDB
========

Installation via Docker
-----------------------
- Install boot2docker
    - http://boot2docker.io/
    - see also https://docs.docker.com/installation/

- Build InfluxDB Docker container::

    boot2docker up
    eval "$(boot2docker shellinit)"
    docker build --tag=influxdb https://raw.githubusercontent.com/crosbymichael/influxdb-docker/master/Dockerfile

Remark:
This Dockerfile pulls the "latest" version, which is InfluxDB 0.8.8 (influxdb-0.8.8.amd64.tar.gz) as of 2015-04-24.
On the other hand, the 0.9 series in the making.



Setup
-----
- Run InfluxDB Docker container::

    boot2docker up
    eval "$(boot2docker shellinit)"

    # 0.8
    docker run --publish=0.0.0.0:8083:8083 --publish=0.0.0.0:8086:8086 --name=influxdb influxdb:latest

    # 0.9
    docker run --publish=0.0.0.0:8083:8083 --publish=0.0.0.0:8086:8086 --name=influxdb09 influxdb/influxdb:latest


Running
-------
::

    # 0.8
    docker start influxdb

    # 0.9
    docker start influxdb09

- Stop and remove Docker container::

    docker stop influxdb
    docker rm influxdb


Configuration
-------------
For configuration, see kotori.node.database.influx

Enable authentication:

https://influxdb.com/docs/v0.9/administration/authentication_and_authorization.html#set-up-authentication

create admin user::

     $ curl --silent --get 'http://192.168.59.103:8086/query?pretty=true' --user root:root --data-urlencode 'q=CREATE USER admin WITH PASSWORD 'admin' WITH ALL PRIVILEGES'

list databases::

     $ curl --silent --get 'http://192.168.59.103:8086/query?pretty=true' --user admin:admin --data-urlencode 'q=SHOW DATABASES' | jq '.'


Query database
--------------

See also:

- https://pypi.python.org/pypi/influxdb
- http://influxdb.com/docs/v0.8/introduction/getting_started.html

Inquire IP address from boot2docker host::

    boot2docker ip
    192.168.59.103

Query database using curl::

    # [0.8] pretty-print json using python
    curl --silent --get 'http://192.168.59.103:8086/db/kotori/series?u=root&p=root' --data-urlencode 'q=select * from telemetry;' | python -mjson.tool

    # [0.8] pretty-print json using jq
    curl --silent --get 'http://192.168.59.103:8086/db/kotori/series?u=root&p=root' --data-urlencode 'q=select * from telemetry;' | jq '.'

    # [0.9] pretty-print json using jq
    curl --silent --get 'http://192.168.59.103:8086/query?pretty=true' --user admin:admin --data-urlencode 'db=hiveeyes_100' --data-urlencode 'q=select * from "1.99";' | jq '.'

    # [0.9] drop database
    curl --silent --get 'http://192.168.59.103:8086/query?pretty=true' --user admin:admin --data-urlencode 'db=hiveeyes_100' --data-urlencode 'q=drop database "hiveeyes_100"'

Query database using Python::

    from influxdb.influxdb08 import InfluxDBClient
    client = InfluxDBClient('192.168.59.103', 8086, 'root', 'root', 'kotori')
    client.query('select * from telemetry;')
