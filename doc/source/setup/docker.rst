.. include:: ../_resources.rst

.. _setup-docker:

##################
Run through Docker
##################


*******
Preface
*******

This part of the documentation covers the installation of Kotori and the whole
software stack for telemetry data acquisition, processing and visualization on
systems running Docker.

The first step to using any software package is getting it properly installed.
Please read this section carefully.

After successfully installing the software, you might want to follow up with
its configuration at :ref:`getting-started`.


************
Introduction
************

This section outlines how to conveniently run Mosquitto, InfluxDB,
MongoDB, Grafana and Kotori using Docker.

The repository provides two files ``docker-compose.yml`` and ``.env``. They
are needed to run the whole foundation infrastructure. On top of that, Kotori
will be run within another container bind-mounting the local ``etc/``
directory in order to bring in the configuration files.

There are two flavors of Kotori Docker images. ``daqzilla/kotori`` includes
all dependencies to run a full installation while ``daqzilla/kotori-standard``
is a more trimmed-down variant, which is also offered for ``arm32v7`` and
``arm64v8`` platforms.

Those images are published to Docker Hub.

- https://hub.docker.com/r/daqzilla/kotori
- https://hub.docker.com/r/daqzilla/kotori-standard

.. note::

    Please note that this Docker Compose configuration is primarily suited for
    evaluation and development purposes. As it either disables authentication
    or uses insecure authentication credentials for Mosquitto, InfluxDB,
    and Grafana, it is not prepared for production setups.


*************
Prerequisites
*************

This will give you Mosquitto, InfluxDB, MongoDB, Grafana, an improved
Grafana map panel plugin, and a command alias for invoking Kotori.

In order to invoke the auxiliary services, run::

    docker compose up

Install Panodata Map Panel plugin into Grafana instance::

    docker exec --interactive kotori_grafana_1 \
        bash -c '
            grafana-cli --pluginUrl https://github.com/panodata/panodata-map-panel/releases/download/0.16.0/panodata-map-panel-0.16.0.zip \
                plugins install panodata-map-panel; \
            pkill grafana-server
        '

Create a command alias for invoking Kotori::

    alias kotori="docker run \
        --volume=$(pwd)/etc:/etc/kotori \
        --publish=24642:24642 \
        --network kotori_default \
        -it --rm daqzilla/kotori \
        kotori"


Preflight checks::

    kotori --version


*********
Testdrive
*********

This is a basic test walkthrough, to check if data is correctly routed from the
telemetry message bus to the database.

InfluxDB
========

This example uses InfluxDB as timeseries-database.

Invoke Kotori::

    kotori --config /etc/kotori/docker/docker-influxdb.ini

Publish single reading using MQTT::

    export CHANNEL_TOPIC=sensorwan-influxdb/foo/bar/1/data.json
    docker run \
        --network kotori_default \
        -it --rm eclipse-mosquitto \
        mosquitto_pub -d -h mosquitto -t $CHANNEL_TOPIC -m '{"temperature": 42.84, "humidity": 83.1}'

Check if reading has been stored in InfluxDB::

    docker run \
        --network kotori_default \
        -it --rm influxdb:1.8 \
        influx -precision=rfc3339 -host=influxdb -database=sensorwan_influxdb_foo -execute='SELECT * FROM bar_1_sensors'

Go to Grafana and visit the dashboard just created::

    open "http://localhost:3000/?orgId=1&search=open&query=sensorwan-influxdb"
