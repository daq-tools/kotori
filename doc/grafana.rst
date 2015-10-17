=======
Grafana
=======


Howtos
======
- http://influxdb.com/docs/v0.8/ui/grafana.html
- http://www.rittmanmead.com/2015/02/obiee-monitoring-and-diagnostics-with-influxdb-and-grafana/
- http://docs.grafana.org/datasources/influxdb/


Installation on Debian
======================
Install package::

    aptitude install apt-transport-https curl

    cat /etc/apt/sources.list.d/grafana.list
    deb https://packagecloud.io/grafana/stable/debian/ wheezy main

    curl https://packagecloud.io/gpg.key | apt-key add -
    aptitude update
    aptitude install grafana


Configure::

    /etc/grafana/grafana.ini
    admin_password = XYZ


Run::
    /etc/init.d/grafana-server start
    tail -F /var/log/grafana/grafana.log






Installation via Docker
=======================
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

    kotori-udp-telemetry-fuzzer
