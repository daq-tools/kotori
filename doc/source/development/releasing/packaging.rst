.. _kotori-package:
.. _kotori-build:

#########
Packaging
#########

.. highlight:: bash


*************
Prerequisites
*************

Prepare baseline Docker images::

    make package-baseline-images

Prepare dependency wheel packages::

    ./packaging/wheels/build.sh
    ./packaging/wheels/upload.sh


***************
Debian packages
***************

Build packages for all targets::

    make package-all version=0.26.6

Build individual packages for Debian and Ubuntu::

    # amd64
    make package-debian flavor=full dist=stretch arch=amd64 version=0.26.6
    make package-debian flavor=full dist=buster arch=amd64 version=0.26.6
    make package-debian flavor=full dist=bionic arch=amd64 version=0.26.6

    # arm64v8
    make package-debian flavor=standard dist=stretch arch=arm64v8 version=0.26.6
    make package-debian flavor=standard dist=buster arch=arm64v8 version=0.26.6

    # arm32v7
    make package-debian flavor=standard dist=stretch arch=arm32v7 version=0.26.6
    make package-debian flavor=standard dist=buster arch=arm32v7 version=0.26.6



*************
Docker images
*************


Authenticate with Docker Hub
============================

We need to do both::

    # Run ``docker login`` to be able to regularly push images.
    docker login

    # Set environment variables because the ``manifest-tool`` requires that.
    export DOCKER_USERNAME=johndoe
    export DOCKER_PASSWORD=supersecret


Build and publish Docker images
===============================

Invoke::

    make package-docker-images version=0.26.6

Run basic QA checks::

    make package-docker-qa tag=0.26.6

Designate specific version as ``latest``::

    make package-docker-link version=0.26.6 tag=latest
