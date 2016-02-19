.. include:: ../_resources.rst

.. _kotori-release:

****************
Kotori releasing
****************

We should adhere to `Semantic Versioning`_.

Cut release
===========

Bump version, tag and push repository, build sdist egg and publish it to eggserver::

    make release bump=minor
