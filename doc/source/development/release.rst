.. include:: ../_resources.rst

.. _kotori-release:

****************
Releasing Kotori
****************

We try to adhere to `Semantic Versioning`_.

Cut release
===========
Bump version in various files, commit them, then tag and push repository::

    make release bump=minor


Build and publish packages
==========================
Build Python sdist egg and publish to egg server::

    make python-package

Build Debian package and publish to package server::

    # build debian package for regular daq flavor (28 MB)
    make debian-package flavor=daq

    # build debian package for advanced daq flavor
    # capable of decoding binary messages (38 MB)
    make debian-package flavor=daq-binary

