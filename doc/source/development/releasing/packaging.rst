.. _kotori-package:
.. _kotori-build:

#############
Run packaging
#############

.. highlight:: bash


*************
Prerequisites
*************
Prepare baseline images::

    make build-debian-stretch-amd64-baseline
    make build-debian-stretch-armhf-baseline

    make build-debian-buster-amd64-baseline
    make build-debian-buster-armhf-baseline

    make build-ubuntu-bionic-amd64-baseline


***************
Debian packages
***************
Build Kotori package::

    # amd64
    make debian-package flavor=full dist=stretch arch=amd64 version=0.24.5
    make debian-package flavor=full dist=buster arch=amd64 version=0.24.5
    make debian-package flavor=full dist=bionic arch=amd64 version=0.24.5

    # armhf
    make debian-package flavor=standard dist=stretch arch=armhf version=0.24.5
    make debian-package flavor=standard dist=buster arch=armhf version=0.24.5


*************
Docker images
*************
::

    make build-dockerhub-image version=0.24.5
    docker login
    docker push daqzilla/kotori
