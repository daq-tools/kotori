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
- https://www.influxdata.com/downloads/#influxdb
- https://s3.amazonaws.com/influxdb/ (deprecated)

Download package
================
::

    # Download package
    wget https://dl.influxdata.com/influxdb/releases/influxdb_1.2.0_amd64.deb

    # Upload to "incoming" directory
    scp influxdb_1.2.0_amd64.deb workbench@packages.example.org:/srv/packages/organizations/elmyra/foss/aptly/public/incoming


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
    wget https://grafanarel.s3.amazonaws.com/builds/grafana_4.2.0-beta1_amd64.deb

    # Download armhf package
    wget https://github.com/fg2it/grafana-on-raspberry/releases/download/v4.2.0-beta1-testing/grafana_4.2.0-beta1_armhf.deb


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
    aptly repo add -config=$APTLY_CONFIG -remove-files=true $APTLY_REPOSITORY $PACKAGES_INCOMING/influxdb_*.deb $PACKAGES_INCOMING/grafana_*.deb

    # Publish repository
    aptly publish update -config=$APTLY_CONFIG -gpg-key=2543A838 -passphrase=esp $APTLY_DISTRIBUTION

