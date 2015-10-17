=============
Grafana setup
=============

Howtos
======
- https://influxdb.com/docs/v0.8/ui/grafana.html
- https://influxdb.com/docs/v0.9/tools/grafana.html
- http://docs.grafana.org/datasources/influxdb/
- http://www.rittmanmead.com/2015/02/obiee-monitoring-and-diagnostics-with-influxdb-and-grafana/


Configuration
=============

Access Grafana
--------------

Go to Grafana's web frontend:

- url:  http://192.168.59.103:3000/
- user: admin
- pass: secret



Add InfluxDB datasource
-----------------------
See also:
http://docs.grafana.org/datasources/influxdb/

- Base settings
    - URL: http://192.168.59.103:3000/datasources/new
    - Name: Kotori Telemetry
    - Default: yes
    - Type: InfluxDB 0.8.x
- Http settings
    - Url: http://192.168.59.103:8086/
    - Access: proxy
- InfluxDB Details
    - Database: kotori
    - User: root
    - Password: root


Add Kotori dashboard
--------------------

Either manually:

- Go to http://192.168.59.103:3000/dashboard/new
- Add Panel » Graph
- Add metric fields

Or by importing:

- http://192.168.59.103:3000/dashboard/import
- doc/grafana-kotori-dashboard.json


View Dashboard:

- http://192.168.59.103:3000/dashboard/db/kotori


Send some testing data
----------------------
::

    h2m-udp-sender
