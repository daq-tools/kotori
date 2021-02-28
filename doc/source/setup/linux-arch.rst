.. include:: ../_resources.rst

.. _setup-arch-linux:

###################
Setup on Arch Linux
###################


*******
Preface
*******

This part of the documentation covers the installation of Kotori and the whole
software stack for telemetry data acquisition, processing and visualization on
an Arch Linux system.

The first step to using any software package is getting it properly installed.
Please read this section carefully.

After successfully installing the software, you might want to follow up with
its configuration at :ref:`getting-started`.


************
Introduction
************

Kotori is not available as an Arch User Repository (AUR) package yet. So, the
installation will use Python's ``pip`` installer to install the Python package
from PyPI.

However, all foundation packages are natively available as Arch Linux packages.


************
Installation
************

Prerequisites
=============

Install Mosquitto, InfluxDB and Grafana::

    pacman -Sy mosquitto influxdb grafana

MongoDB is provided through the Arch User Repository (AUR)::

    # Install Git in order to touch AUR
    pacman -Sy git

    # Install MongoDB daemon
    git clone https://aur.archlinux.org/mongodb-bin
    cd mongodb-bin
    makepkg -si

    # Install MongoDB tools
    git clone https://aur.archlinux.org/mongodb-tools-bin
    cd mongodb-tools-bin
    makepkg -si


Kotori
======
::

    # Install Python and pip
    pacman -Sy python python-pip

    # Install Kotori
    pip install --user kotori

Testdrive::

    kotori --version
