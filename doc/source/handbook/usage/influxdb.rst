.. _influxdb-handbook:

========
InfluxDB
========

.. admonition:: Please note

    This page is just a stub.


- https://docs.influxdata.com/influxdb/v1.1/query_language/spec/

::

    export INFLUXDB_HOST=daq.example.org


Authentication
--------------

Enable auth-only access by creating admin user::

    $ curl --silent --get 'http://$INFLUXDB_HOST:8086/query?pretty=true' --user root:root --data-urlencode 'q=CREATE USER admin WITH PASSWORD 'admin' WITH ALL PRIVILEGES'

.. seealso:: https://docs.influxdata.com/influxdb/v1.1/query_language/authentication_and_authorization/



Database operations
-------------------
Create database::

    curl --silent --get 'http://$INFLUXDB_HOST:8086/query?pretty=true' --user admin:admin --data-urlencode 'q=CREATE DATABASE "hiveeyes_100"'


List databases::

    curl --silent --get 'http://$INFLUXDB_HOST:8086/query?pretty=true' --user admin:admin --data-urlencode 'q=SHOW DATABASES' | jq '.'


Drop database::

    curl --silent --get 'http://$INFLUXDB_HOST:8086/query?pretty=true' --user admin:admin --data-urlencode 'q=DROP DATABASE "hiveeyes_100"'

Write data
----------

.. seealso:: https://docs.influxdata.com/influxdb/v1.1/guides/writing_data/


Query operations
----------------

Inquire IP address from boot2docker host::

    boot2docker ip
    $INFLUXDB_HOST

Query database using curl::

    # pretty-print json using jq
    curl --silent --get 'http://$INFLUXDB_HOST:8086/query?pretty=true' --user admin:admin --data-urlencode 'db=hiveeyes_100' --data-urlencode 'q=select * from "1.99";' | jq '.'

.. seealso:: https://docs.influxdata.com/influxdb/v1.1/guides/querying_data/


Querying from Python
--------------------
::

    from influxdb.client import InfluxDBClient
    client = InfluxDBClient('$INFLUXDB_HOST', 8086, 'root', 'root', 'kotori')
    client.query('select * from telemetry;')

.. seealso:: https://pypi.python.org/pypi/influxdb


Backup and Restore
------------------
Backup example::

    influxd backup -database hiveeyes_25a0e5df_9517_405b_ab14_cb5b514ac9e8 -host swarm.hiveeyes.org:8088 hiveeyes_25a0e5df_9517_405b_ab14_cb5b514ac9e8

Restore example::

    influxd restore -datadir /var/lib/influxdb/data -database hiveeyes_25a0e5df_9517_405b_ab14_cb5b514ac9e8 hiveeyes_25a0e5df_9517_405b_ab14_cb5b514ac9e8


.. seealso:: https://docs.influxdata.com/influxdb/v1.1/administration/backup_and_restore/


Export and Import
-----------------
CSV-based import and export using https://github.com/jpillora/csv-to-influxdb.

Export::

    http GET https://swarm.hiveeyes.org/api/hiveeyes/25a0e5df-9517-405b-ab14-cb5b514ac9e8/3756782252718325761/1/data.csv from=2016-01-01 --download

Import::

    export GOPATH=`pwd`
    go get -v github.com/jpillora/csv-to-influxdb

    ./bin/csv-to-influxdb --batch-size=1 --timestamp-column=time --timestamp-format="2006-01-02 15:04:05.000000000" --server=http://localhost:8086 --database=hiveeyes_25a0e5df_9517_405b_ab14_cb5b514ac9e8 --measurement=3756782252718325761_1 ../../data/25a0e5df_9517_405b_ab14_cb5b514ac9e8_3756782252718325761_1_20160101T000000_20160705T195237.csv
    2016/07/05 21:55:15 Done (wrote 34304 points)


- If you like Python, see https://github.com/fabio-miranda/csv-to-influxdb
- If you like Javascript, see https://github.com/CorpGlory/csv2influx
