=======
Grafana
=======


Howtos
------
- http://influxdb.com/docs/v0.8/ui/grafana.html
- http://www.rittmanmead.com/2015/02/obiee-monitoring-and-diagnostics-with-influxdb-and-grafana/
- http://docs.grafana.org/datasources/influxdb/


Installation via Docker
-----------------------
See also: http://docs.grafana.org/installation/docker/
::

    boot2docker up
    eval "$(boot2docker shellinit)"

    docker run \
        --name=grafana \
        --detach=false \
        --publish=3000:3000 \
        --volume=/var/lib/grafana:/var/lib/grafana \
        --env='GF_SECURITY_ADMIN_PASSWORD=secret' \
        grafana/grafana:latest

        #--volume=/etc/grafana:/etc/grafana \


Configuration
-------------
Open configuration file in editor::

    nano /etc/grafana/config.js

Uncomment the InfluxDB stanzas and amend them as follows::

    datasources: {
        influxdb: {
            type: 'influxdb',
            url: "http://sampleapp:8086/db/carbon",
            username: 'root',
            password: 'root',
        },
        grafana: {
            type: 'influxdb',
            url: "http://sampleapp:8086/db/grafana",
            username: 'root',
            password: 'root',
            grafanaDB: true
        },
    },


Access Grafana
--------------

Go to http://192.168.59.103:3000/
user: admin
pass: secret


Add InfluxDB datasource
-----------------------
http://docs.grafana.org/datasources/influxdb/

http://192.168.59.103:3000/datasources/new
Name: Kotori Telemetry
Default: yes
Type: InfluxDB 0.8.x

Http settings
Url: http://192.168.59.103:8086/
Access: proxy

InfluxDB Details
Database: kotori
User: root
Password: root


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

    kotori-udp-telemetry-fuzzer

