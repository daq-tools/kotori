.. _foundation-packages:

###################
Foundation packages
###################

.. contents::
   :local:
   :depth: 1

----


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
    wget https://dl.influxdata.com/influxdb/releases/influxdb_1.2.2_amd64.deb

    # Download armhf packages
    wget http://ftp.de.debian.org/debian/pool/main/i/influxdb/influxdb_1.1.1+dfsg1-4_armhf.deb
    wget http://ftp.de.debian.org/debian/pool/main/i/influxdb/influxdb-client_1.1.1+dfsg1-4_armhf.deb

    # Upload to "incoming" directory
    scp influxdb_*.deb workbench@packages.example.org:/srv/packages/organizations/elmyra/foss/aptly/public/incoming


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
    wget https://s3-us-west-2.amazonaws.com/grafana-releases/release/grafana_4.2.0_amd64.deb

    # Download armhf package
    wget https://github.com/fg2it/grafana-on-raspberry/releases/download/v4.2.0/grafana_4.2.0_armhf.deb

    # Upload to "incoming" directory
    scp grafana_4.2.0-beta1_*.deb workbench@packages.example.org:/srv/packages/organizations/elmyra/foss/aptly/public/incoming


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
    aptly repo add -config=$APTLY_CONFIG -remove-files=true $APTLY_REPOSITORY $PACKAGES_INCOMING/influxdb*.deb $PACKAGES_INCOMING/grafana_*.deb

    # Publish repository
    aptly publish update -config=$APTLY_CONFIG -gpg-key=2543A838 -passphrase=esp $APTLY_DISTRIBUTION

