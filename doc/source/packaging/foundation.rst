.. _foundation-packages:

###################
Foundation packages
###################


********
InfluxDB
********
- https://s3.amazonaws.com/influxdb/
- https://www.influxdata.com/downloads/#influxdb

Get fresh package
=================
::

    # Download package
    wget https://dl.influxdata.com/influxdb/releases/influxdb_1.2.0_amd64.deb

    # Upload to "incoming" directory
    scp influxdb_1.2.0_amd64.deb workbench@packages.example.org:/srv/packages/organizations/elmyra/foss/aptly/public/incoming


Publish package
===============
::

    ssh workbench@packages.example.org

    export APTLY_CONFIG=/srv/packages/organizations/elmyra/foss/aptly/aptly.conf
    export APTLY_REPOSITORY=foundation
    export APTLY_DISTRIBUTION=testing
    export PACKAGES_INCOMING=/srv/packages/organizations/elmyra/foss/aptly/public/incoming

    # Add packages to repository
    aptly repo add -config=$APTLY_CONFIG -remove-files=true $APTLY_REPOSITORY $PACKAGES_INCOMING/influxdb_*.deb

    # Publish repository
    aptly publish update -config=$APTLY_CONFIG -gpg-key=2543A838 -passphrase=esp $APTLY_DISTRIBUTION



*******
Grafana
*******
- https://packagecloud.io/grafana/stable
- http://grafana.org/builds/
- https://github.com/fg2it/grafana-on-raspberry/releases

