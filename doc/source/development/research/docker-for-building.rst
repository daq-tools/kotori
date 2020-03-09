**********************************
Using Docker for building packages
**********************************

Leverage multi-CPU architecture support
=======================================
Docker brings multi-CPU architecture support:

    Docker images can support multiple architectures, which means that a single
    image may contain variants for different architectures, and sometimes for
    different operating systems, such as Windows.

    When running an image with multi-architecture support, docker will
    automatically select an image variant which matches your OS and architecture.

    Most of the official images on Docker Hub provide a variety of architectures.
    For example, the busybox image supports ``amd64``, ``arm32v5``, ``arm32v6``,
    ``arm32v7``, ``arm64v8``, ``i386``, ``ppc64le`` and ``s390x``.

    Docker Desktop for Mac provides ``binfmt_misc`` multi-architecture support,
    which means you can run containers for different Linux architectures such as
    ``arm``, ``mips``, ``ppc64le`` and even ``s390x``.

    This does not require any special configuration in the container itself as it
    uses qemu-static from the Docker for Mac VM. Because of this, you can run an
    ARM container, like the ``arm32v7`` or ``ppc64le`` variants of the busybox image.

    | -- https://docs.docker.com/docker-for-mac/multi-arch/
    | -- https://github.com/docker-library/official-images#architectures-other-than-amd64


Hands-on
========
Emulating ARM::

      docker run -it --rm arm32v7/debian:stretch-slim uname -a
      docker run -it --rm balenalib/armv7hf-debian:stretch-build uname -a

Miscellaneous
=============
- https://ownyourbits.com/2018/06/27/running-and-building-arm-docker-containers-in-x86/
- https://blog.hypriot.com/post/test-build-and-package-docker-for-arm-the-official-way/
- https://blog.hypriot.com/post/setup-simple-ci-pipeline-for-arm-images/
- https://www.balena.io/blog/building-arm-containers-on-any-x86-machine-even-dockerhub/
- https://www.ecliptik.com/Cross-Building-and-Running-Multi-Arch-Docker-Images/
- https://hub.docker.com/u/arm32v7/
- https://hub.docker.com/r/arm32v7/debian
- https://github.com/hypriot/arm-compose
- https://forums.docker.com/t/build-a-container-for-arm-architecture/34266
- https://hub.docker.com/r/budry/registry-arm/
- https://marina.io/
- https://hub.docker.com/r/resin/rpi-raspbian/
- https://www.balena.io/docs/reference/base-images/base-images/
- https://www.balena.io/docs/reference/base-images/devicetypes/
- https://hub.docker.com/r/balenalib/armv7hf-debian-python
- https://github.com/docker-library/official-images
- https://github.com/balena-io-library/official-images/tree/master/library
- https://docs.docker.com/develop/develop-images/multistage-build/
- https://medium.com/@tonistiigi/advanced-multi-stage-build-patterns-6f741b852fae

Non-Docker things
=================
- https://github.com/debuerreotype/debuerreotype
- https://docs.armbian.com/Developer-Guide_Using-Vagrant/
- https://github.com/adafruit/ARM-toolchain-vagrant/blob/master/Vagrantfile
- https://stackoverflow.com/questions/34051322/is-there-a-vagrant-box-that-simulates-a-raspberry-pi
- https://github.com/twobitcircus/rpi-build-and-boot
- https://github.com/Asquera/raspberry-devbox
- https://developer.mozilla.org/en-US/docs/Mozilla/Developer_guide/Virtual_ARM_Linux_environment
- https://github.com/DieterReuter/qemu-arm-box
