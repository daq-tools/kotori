.. _foundation-packages:

###################
Foundation packages
###################

.. contents::
   :local:
   :depth: 1

----


*********
Mosquitto
*********
- http://repo.mosquitto.org/debian/pool/main/m/mosquitto/

Download packages
=================
::

    # Download amd64 packages
    wget http://repo.mosquitto.org/debian/pool/main/m/mosquitto/mosquitto_1.6.1-0mosquitto1_amd64.deb
    wget http://repo.mosquitto.org/debian/pool/main/m/mosquitto/mosquitto-clients_1.6.1-0mosquitto1_amd64.deb
    wget http://repo.mosquitto.org/debian/pool/main/m/mosquitto/libmosquitto1_1.6.1-0mosquitto1_amd64.deb

    # Download armhf packages
    wget http://repo.mosquitto.org/debian/pool/main/m/mosquitto/mosquitto_1.6.1-0mosquitto1_armhf.deb
    wget http://repo.mosquitto.org/debian/pool/main/m/mosquitto/mosquitto-clients_1.6.1-0mosquitto1_armhf.deb
    wget http://repo.mosquitto.org/debian/pool/main/m/mosquitto/libmosquitto1_1.6.1-0mosquitto1_armhf.deb

    # Upload to "incoming" directory
    scp mosquitto*.deb workbench@packages.example.org:/srv/packages/organizations/elmyra/foss/aptly/public/incoming


********
InfluxDB
********
- https://portal.influxdata.com/downloads
- http://ftp.de.debian.org/debian/pool/main/i/influxdb/
- https://s3.amazonaws.com/influxdb/ (deprecated)

Download packages
=================
::

    # Download amd64 package
    wget https://dl.influxdata.com/influxdb/releases/influxdb_1.7.6_amd64.deb

    # Download armhf packages
    wget https://dl.influxdata.com/influxdb/releases/influxdb_1.7.6_armhf.deb

    # Upload to "incoming" directory
    scp influxdb_*.deb workbench@packages.example.org:/srv/packages/organizations/elmyra/foss/aptly/public/incoming

Deprecated::

    wget http://ftp.de.debian.org/debian/pool/main/i/influxdb/influxdb_1.1.1+dfsg1-4_armhf.deb
    wget http://ftp.de.debian.org/debian/pool/main/i/influxdb/influxdb-client_1.1.1+dfsg1-4_armhf.deb


*******
Grafana
*******
- https://packagecloud.io/grafana/stable
- http://grafana.org/builds/
- https://github.com/fg2it/grafana-on-raspberry/releases


Download package
================
::

    # Download amd64 package
    wget https://dl.grafana.com/oss/release/grafana_5.4.4_amd64.deb

    # Download armhf package
    wget https://dl.grafana.com/oss/release/grafana_5.4.4_armhf.deb

    # Upload to "incoming" directory
    scp grafana_*.deb workbench@packages.example.org:/srv/packages/organizations/elmyra/foss/aptly/public/incoming


Deprecated::

    # Download armhf package
    wget https://github.com/fg2it/grafana-on-raspberry/releases/download/v4.2.0/grafana_4.2.0_armhf.deb



****************
Publish packages
****************
::

    ssh workbench@packages.example.org

    export APTLY_CONFIG=/srv/packages/organizations/elmyra/foss/aptly/aptly.conf
    export APTLY_REPOSITORY=foundation
    export APTLY_DISTRIBUTION=testing
    export PACKAGES_INCOMING=/srv/packages/organizations/elmyra/foss/aptly/public/incoming

    # Add packages to repository
    aptly repo add -config=$APTLY_CONFIG -remove-files=true $APTLY_REPOSITORY \
        $PACKAGES_INCOMING/influxdb*.deb $PACKAGES_INCOMING/grafana*.deb $PACKAGES_INCOMING/*mosquitto*.deb

    # Publish repository
    aptly publish update -config=$APTLY_CONFIG -gpg-key=2543A838 -passphrase=esp $APTLY_DISTRIBUTION
