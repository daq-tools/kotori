.. include:: ../_resources.rst

.. _setup-docker:

##################
Run through Docker
##################


*************
Prerequisites
*************
Run Mosquitto::

    docker run \
        --name=mosquitto \
        --detach=true \
        -tip 1883:1883 -p 9001:9001 \
        eclipse-mosquitto:1.6.8

Run InfluxDB::

    docker run \
        --name=influxdb \
        --detach=true \
        --publish 8083:8083 --publish 8086:8086 \
        --volume="$(pwd)/var/lib/influxdb":/var/lib/influxdb \
        influxdb:1.7.10

Run Grafana::

    docker run \
        --name=grafana \
        --detach=true \
        --publish=3000:3000 \
        --link influxdb:influxdb \
        --volume="$(pwd)/var/lib/grafana":/var/lib/grafana \
        --env='GF_SECURITY_ADMIN_PASSWORD=admin' \
        grafana/grafana:6.6.2

        #--volume=/etc/grafana:/etc/grafana \

Setup Grafana Map Panel::

    docker exec -i grafana grafana-cli \
        --pluginUrl https://packages.hiveeyes.org/grafana/grafana-map-panel/grafana-map-panel-0.9.0.zip \
        plugins install grafana-map-panel

    docker restart grafana


Run MongoDB::

    docker run \
        --name=mongodb \
        --detach=true \
        --publish 27017:27017 \
        --volume="$(pwd)/var/lib/mongodb":/var/lib/mongodb \
        mongo:4.2.3


After provisioning, these instances can be spinned up again by invoking::

    docker start mosquitto influxdb grafana mongodb


******
Kotori
******
Running Kotori through Docker is easy.

Check if installation works::

    docker run -it --rm daqzilla/kotori kotori --version

Invoke Kotori container linked to the other containers::

    docker run \
        --volume="$(pwd)/etc":/etc/kotori \
        --publish=24642:24642 \
        --link mosquitto:mosquitto \
        --link influxdb:influxdb \
        --link grafana:grafana \
        --link mongodb:mongodb \
        -it --rm daqzilla/kotori \
        kotori --config /etc/kotori/docker-mqttkit.ini

Submit single reading::

    export CHANNEL_TOPIC=mqttkit-1/foo/bar/1/data.json
    docker run \
        --link mosquitto:mosquitto \
        -it --rm eclipse-mosquitto:1.6.8 \
        mosquitto_pub -h mosquitto -t $CHANNEL_TOPIC -m '{"temperature": 42.84, "humidity": 83.1}'

Check if reading has been stored in InfluxDB::

    docker run \
        --link influxdb:influxdb \
        -it --rm influxdb:1.7.10 \
        influx -precision=rfc3339 -host=influxdb -database=mqttkit_1_foo -execute='SELECT * FROM bar_1_sensors'
