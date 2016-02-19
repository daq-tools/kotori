==================
Configure InfluxDB
==================


Authentication
--------------

Purpose: Enable auth-only access to InfluxDB.

.. highlight:: bash

#. Create admin user::

    $ curl --silent --get 'http://192.168.59.103:8086/query?pretty=true' --user root:root --data-urlencode 'q=CREATE USER admin WITH PASSWORD 'admin' WITH ALL PRIVILEGES'

.. highlight:: ini

#. Enable authentication by setting the ``auth-enabled`` option to true in the ``[http]`` section of the configuration file::

    [http]
    # ...
    auth-enabled = true
    # ...



.. seealso::
    - `InfluxDB docs: Set up authentication <https://influxdb.com/docs/v0.9/administration/authentication_and_authorization.html#set-up-authentication>`_
    - :ref:`influxdb-handbook`


Backup
------
- https://github.com/influxdata/influxdb/issues/5443
- https://github.com/influxdata/influxdb/pull/5467/files
- https://github.com/influxdata/influxdb/issues/5451
- https://github.com/influxdata/influxdb/issues/5446
- https://docs.influxdata.com/influxdb/v0.9/administration/backup_and_restore/
