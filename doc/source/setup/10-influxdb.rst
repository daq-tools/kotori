========
InfluxDB
========


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
