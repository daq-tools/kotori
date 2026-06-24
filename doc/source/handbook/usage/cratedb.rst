.. include:: ../../_resources.rst

.. _cratedb-handbook:

################
CrateDB handbook
################

.. todo:: Content on this page may need an enrichment.

This section of the documentation will give you a short and concise summary about
how to operate CrateDB, and how to use it.

Unless we have more to report here, please refer to the upstream documentation.

- `Installing CrateDB`_
- `Using CrateDB`_
- `CrateDB reference documentation`_
- `Overview of CrateDB drivers and adapters`_
- `Overview of CrateDB integration tutorials`_

The most easy way to run CrateDB on your workstation for evaluation purposes, is
to use Podman or Docker.

::

    docker run --rm -it \
        --publish=4200:4200 --publish=5432:5432 \
        --env=CRATE_HEAP_SIZE=4g \
        crate:5.2 -Cdiscovery.type=single-node

.. _CrateDB reference documentation: https://crate.io/docs/crate/reference/
.. _Installing CrateDB: https://crate.io/docs/crate/tutorials/
.. _Overview of CrateDB drivers and adapters: https://community.crate.io/t/overview-of-cratedb-drivers-and-adapters/1464
.. _Overview of CrateDB integration tutorials: https://community.crate.io/t/overview-of-cratedb-integration-tutorials/1015
.. _Using CrateDB: https://crate.io/docs/crate/howtos/
