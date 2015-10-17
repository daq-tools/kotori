========================
Kotori DAQ sandbox setup
========================

Global python packages
----------------------
::

    # maybe
    pip install Twisted



InfluxDB
========

Installation via Docker
-----------------------
- Install boot2docker
    - http://boot2docker.io/
    - see also https://docs.docker.com/installation/

- Build InfluxDB Docker container::

    boot2docker up
    eval "$(boot2docker shellinit)"
    docker build --tag=influxdb https://raw.githubusercontent.com/crosbymichael/influxdb-docker/master/Dockerfile

Remark:
This Dockerfile pulls the "latest" version, which is InfluxDB 0.8.8 (influxdb-0.8.8.amd64.tar.gz) as of 2015-04-24.
On the other hand, the 0.9 series in the making.



Setup
-----
- Run InfluxDB Docker container::

    boot2docker up
    eval "$(boot2docker shellinit)"

    # 0.8
    docker run --publish=0.0.0.0:8083:8083 --publish=0.0.0.0:8086:8086 --name=influxdb influxdb:latest

    # 0.9
    docker run --publish=0.0.0.0:8083:8083 --publish=0.0.0.0:8086:8086 --name=influxdb09 influxdb/influxdb:latest


Running
-------
::

    boot2docker up
    eval "$(boot2docker shellinit)"

    # 0.8
    docker start influxdb

    # 0.9
    docker start influxdb09

- Stop and remove Docker container::

    docker stop influxdb
    docker rm influxdb


Grafana
=======
See also: http://docs.grafana.org/installation/docker/


Installation via Docker
-----------------------
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
