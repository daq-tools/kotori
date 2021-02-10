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

    make package-baseline-images


***************
Debian packages
***************

Build packages for all targets::

    make package-all

Build individual packages for Debian and Ubuntu::

    # amd64
    make package-debian flavor=full dist=stretch arch=amd64 version=0.24.5
    make package-debian flavor=full dist=buster arch=amd64 version=0.24.5
    make package-debian flavor=full dist=bionic arch=amd64 version=0.24.5

    # armv7hf
    make package-debian flavor=standard dist=stretch arch=armv7hf version=0.24.5
    make package-debian flavor=standard dist=buster arch=armv7hf version=0.24.5


*************
Docker images
*************
::

    make package-dockerhub-image version=0.24.5
    docker login
    docker push daqzilla/kotori
