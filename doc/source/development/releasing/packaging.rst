.. _kotori-package:
.. _kotori-build:

#########
Packaging
#########

.. highlight:: bash


*************
Prerequisites
*************

The package build system is based on `Docker`_, please read the documentation
at `Install Docker`_ how to set it up on your system.

For example, on Debian 11 (bullseye), you would install it like this::

    # Acquire package signing key.
    wget -qO - https://download.docker.com/linux/debian/gpg | apt-key add -

    # Register with package repository.
    echo "deb [arch=amd64] https://download.docker.com/linux/debian bullseye stable" > /etc/apt/sources.list.d/docker.list
    apt-get update

    # Install Docker.
    apt-get install docker-ce

After installing Docker, some additional packages are needed::

    apt-get install python3 python3-venv git make qemu-user-static binfmt-support

Then, get hold of the sources and install a minimum part of the sandbox::

    git clone https://github.com/daq-tools/kotori
    cd kotori
    make install-releasetools


***************
Baseline images
***************

Prepare baseline Docker images::

    make package-baseline-images

Optionally, prepare dependency wheel packages (most users can skip this step)::

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


.. _Docker: https://docker.com/
.. _Install Docker: https://docs.docker.com/get-docker/
