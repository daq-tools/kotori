.. include:: ../_resources.rst

.. _docker-infrastructure:

=============================
Docker infrastructure sandbox
=============================

Global python packages
----------------------
::

    # maybe
    pip install Twisted


Boot2Docker
===========
... is only required for ancient Mac OSX releases.

- http://boot2docker.io/
- https://github.com/boot2docker

Installation
------------
- Install boot2docker
    - http://boot2docker.io/
    - see also https://docs.docker.com/installation/

Start
-----
::

    boot2docker up
    eval "$(boot2docker shellinit)"


InfluxDB
========
.. seealso::

    - https://hub.docker.com/_/influxdb/

Setup
-----
- Run InfluxDB Docker container::

    docker pull influxdb:1.2.2

    docker run --name=influxdb-1.2.2 --detach=true --publish 8083:8083 --publish 8086:8086 influxdb:1.2.2


Running
-------
::

    boot2docker up
    eval "$(boot2docker shellinit)"

    docker start influxdb

- Stop and remove Docker container::

    docker stop influxdb
    docker rm influxdb


Grafana
=======
.. seealso::

    - https://hub.docker.com/r/grafana/grafana/
    - http://docs.grafana.org/installation/docker/


Installation via Docker
-----------------------
::

    docker pull grafana/grafana:4.2.0

    docker run \
        --name=grafana-4.2.0 \
        --detach=true \
        --publish=3000:3000 \
        --volume=/var/lib/grafana:/var/lib/grafana \
        --env='GF_SECURITY_ADMIN_PASSWORD=secret' \
        grafana/grafana:4.2.0

        #--volume=/etc/grafana:/etc/grafana \

Setup Worldmap Panel::

    docker exec -i grafana-4.2.0 grafana-cli plugins install grafana-worldmap-panel
    docker restart grafana-4.2.0


Running
-------
::

    docker start grafana


Upgrading
---------
::

    docker_remote_tags grafana/grafana
    docker pull grafana/grafana

.. seealso:: https://bitbucket.org/denilsonsa/small_scripts/src/default/docker_remote_tags.sh


Mosquitto
=========

https://github.com/toke/docker-mosquitto

First time::

    boot2docker up
    eval "$(boot2docker shellinit)"
    docker run -tip 1883:1883 -p 9001:9001 --name=mosquitto toke/mosquitto

Regular::

    boot2docker up
    eval "$(boot2docker shellinit)"
    docker start mosquitto

Inquire IP address from boot2docker host::

    boot2docker ip
    192.168.59.103
