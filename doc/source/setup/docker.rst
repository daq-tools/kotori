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

This section outlines how to conveniently run Mosquitto, InfluxDB, MongoDB,
Grafana and Kotori using Docker.

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
    or uses insecure authentication credentials for Mosquitto, InfluxDB and
    Grafana, it is not prepared for production setups.


*************
Prerequisites
*************

This will give you Mosquitto, InfluxDB, MongoDB and Grafana as well as an
improved Grafana map panel plugin.

Just invoke::

    docker-compose up

Setup Panodata Map panel plugin::

    docker exec --interactive kotori_grafana_1 \
        bash -c '
            grafana-cli --pluginUrl https://github.com/panodata/grafana-map-panel/releases/download/0.15.0/grafana-map-panel-0.15.0.zip \
                plugins install grafana-map-panel; \
            pkill grafana-server
        '


******
Kotori
******
Running Kotori through Docker is easy.

Preflight checks::

    docker run -it --rm daqzilla/kotori kotori --version

Invoke Kotori::

    docker run \
        --volume="$(pwd)/etc":/etc/kotori \
        --publish=24642:24642 \
        --network kotori_default \
        -it --rm daqzilla/kotori \
        kotori --config /etc/kotori/docker.ini


*********
Testdrive
*********
This is a basic test to check if data is flowing correctly between the subsystems.

Submit single reading::

    export CHANNEL_TOPIC=mqttkit-1/foo/bar/1/data.json
    docker run \
        --network kotori_default \
        -it --rm eclipse-mosquitto:1.6 \
        mosquitto_pub -h mosquitto -t $CHANNEL_TOPIC -m '{"temperature": 42.84, "humidity": 83.1}'

Check if reading has been stored in InfluxDB::

    docker run \
        --network kotori_default \
        -it --rm influxdb:1.8 \
        influx -precision=rfc3339 -host=influxdb -database=mqttkit_1_foo -execute='SELECT * FROM bar_1_sensors'

Go to Grafana and visit the dashboard just created::

    open "http://localhost:3000/?orgId=1&search=open&query=mqttkit"
