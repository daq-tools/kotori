#######################
Secure the installation
#######################


Close ports
-----------

/etc/grafana/grafana.ini::

    http_addr = localhost

::

    systemctl restart grafana-server

/etc/opt/influxdb/influxdb.conf::

    [admin]
    bind-address = "localhost:8083"

    [http]
    bind-address = "localhost:8086"

    [meta]
    bind-address = "localhost:8088"

::

    systemctl restart influxdb


Nginx
-----
Todo.

- Configuration
- Let's Encrypt
