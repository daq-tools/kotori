#######################
Secure the installation
#######################


Close ports
===========

InfluxDB
--------

/etc/influxdb/influxdb.conf::

    # Outside of any scope
    bind-address = "localhost:8088"

    [admin]
    bind-address = "localhost:8083"

    [http]
    bind-address = "localhost:8086"

    [meta]
    bind-address = "localhost:8088"

::

    systemctl restart influxdb


Grafana
-------

/etc/grafana/grafana.ini::

    http_addr = localhost

::

    systemctl restart grafana-server



Enable authentication
=====================

InfluxDB
--------
Purpose: Enable auth-only access to InfluxDB.

.. highlight:: bash

#. Create admin user::

    $ curl --silent --get 'http://kotori.example.org:8086/query?pretty=true' --user root:root --data-urlencode 'q=CREATE USER admin WITH PASSWORD 'admin' WITH ALL PRIVILEGES'

.. highlight:: ini

#. Enable authentication by setting the ``auth-enabled`` option to true in the ``[http]`` section of the configuration file::

    [http]
    # ...
    auth-enabled = true
    # ...

.. seealso::

    - `InfluxDB docs: Set up authentication <https://docs.influxdata.com/influxdb/v1.8/administration/authentication_and_authorization/>`_
    - :ref:`influxdb-handbook`
