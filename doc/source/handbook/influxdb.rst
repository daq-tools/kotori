.. _influxdb-handbook:

========================
Kotori InfluxDB Handbook
========================


Authentication
--------------

Enable auth-only access by creating admin user::

    $ curl --silent --get 'http://192.168.59.103:8086/query?pretty=true' --user root:root --data-urlencode 'q=CREATE USER admin WITH PASSWORD 'admin' WITH ALL PRIVILEGES'

.. seealso:: https://influxdb.com/docs/v0.9/administration/authentication_and_authorization.html#set-up-authentication



Database operations
-------------------
Create database::

    curl --silent --get 'http://192.168.59.103:8086/query?pretty=true' --user admin:admin --data-urlencode --data-urlencode 'q=CREATE DATABASE "hiveeyes_100"'


List databases::

    curl --silent --get 'http://192.168.59.103:8086/query?pretty=true' --user admin:admin --data-urlencode 'q=SHOW DATABASES' | jq '.'


Drop database::

    curl --silent --get 'http://192.168.59.103:8086/query?pretty=true' --user admin:admin --data-urlencode 'db=hiveeyes_100' --data-urlencode 'q=DROP DATABASE "hiveeyes_100"'


Query operations
----------------

Inquire IP address from boot2docker host::

    boot2docker ip
    192.168.59.103

Query database using curl::

    # pretty-print json using jq
    curl --silent --get 'http://192.168.59.103:8086/query?pretty=true' --user admin:admin --data-urlencode 'db=hiveeyes_100' --data-urlencode 'q=select * from "1.99";' | jq '.'

.. seealso:: https://influxdb.com/docs/v0.9/guides/writing_data.html


Querying from Python
--------------------
::

    from influxdb.client import InfluxDBClient
    client = InfluxDBClient('192.168.59.103', 8086, 'root', 'root', 'kotori')
    client.query('select * from telemetry;')

.. seealso:: https://pypi.python.org/pypi/influxdb
