==============
InfluxDB setup
==============


Authentication
--------------
For configuration, see kotori.node.database.influx

Enable authentication:

https://influxdb.com/docs/v0.9/administration/authentication_and_authorization.html#set-up-authentication

create admin user::

    # [0.9]
    $ curl --silent --get 'http://192.168.59.103:8086/query?pretty=true' --user root:root --data-urlencode 'q=CREATE USER admin WITH PASSWORD 'admin' WITH ALL PRIVILEGES'



Administer database
-------------------
create database::

    # [0.9]
    curl --silent --get 'http://192.168.59.103:8086/query?pretty=true' --user admin:admin --data-urlencode --data-urlencode 'q=CREATE DATABASE "hiveeyes_100"'


list databases::

    # [0.9]
    curl --silent --get 'http://192.168.59.103:8086/query?pretty=true' --user admin:admin --data-urlencode 'q=SHOW DATABASES' | jq '.'


drop database::

    # [0.9]
    curl --silent --get 'http://192.168.59.103:8086/query?pretty=true' --user admin:admin --data-urlencode 'db=hiveeyes_100' --data-urlencode 'q=DROP DATABASE "hiveeyes_100"'


Querying via HTTP
-----------------
See also:
https://influxdb.com/docs/v0.9/guides/writing_data.html

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


Querying from Python
--------------------
See also:

- https://pypi.python.org/pypi/influxdb

::

    from influxdb.influxdb08 import InfluxDBClient
    client = InfluxDBClient('192.168.59.103', 8086, 'root', 'root', 'kotori')
    client.query('select * from telemetry;')
