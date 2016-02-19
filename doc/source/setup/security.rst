#######################
Secure the installation
#######################

Close ports
===========

InfluxDB
--------

/etc/opt/influxdb/influxdb.conf::

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

https://influxdb.com/docs/v0.9/administration/authentication_and_authorization.html#set-up-authentication

create admin user::

     $ curl --silent --get 'http://swarm.hiveeyes.org:8086/query?pretty=true' --user root:root --data-urlencode 'q=CREATE USER admin WITH PASSWORD 'Armoojwi' WITH ALL PRIVILEGES'


Nginx
-----
Todo.

- Configuration
- Let's Encrypt
