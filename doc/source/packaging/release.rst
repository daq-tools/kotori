.. include:: ../_resources.rst

.. _kotori-release:

****************
Releasing Kotori
****************

The designated public Debian repository host is ``pulp.cicer.de``. It is currently running Debian Jessie (8.4).

Cut release
===========
Bump version number in various files, commit them, add tag reflecting the version number and finally push the repository to its origin::

    make release bump=minor

.. note:: We try to adhere to `Semantic Versioning`_.


Build and upload packages
=========================
Build Python sdist egg and publish to egg server::

    make python-package

Build Debian package and upload to the package server ``/incoming`` directory, the package version is taken from ``setup.py``::

    # build debian package for regular daq flavor (28 MB)
    make debian-package flavor=daq

    # build debian package for advanced daq flavor
    # capable of decoding binary messages (38 MB)
    make debian-package flavor=daq-binary

After doing so, the package should appear at https://packages.elmyra.de/elmyra/foss/debian/incoming/.


Publish package to Debian repository
====================================
::

    ssh workbench@pulp.cicer.de
    cd /srv/packages/organizations/elmyra/foss/aptly
    aptly repo add -config=aptly.conf testing public/incoming/kotori_0.7.0-1_amd64.deb
    aptly publish update -config=aptly.conf -gpg-key=2543A838 -passphrase=esp testing

.. note:: How to setup the :ref:`kotori-setup`.

