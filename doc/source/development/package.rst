.. include:: ../_resources.rst

.. _kotori-package:

****************
Kotori packaging
****************

The designated Debian buildslave is ``oasis.cicer.de``. It is running Debian 8.3 aka. Debian Jessie.

Prepare buildslave
==================
Install packages::

    apt-get install aptitude
    aptitude update && aptitude upgrade

    # system
    aptitude install fail2ban

    # development
    aptitude install git

    # header files
    aptitude install build-essential python-dev ruby-dev libssl-dev libffi-dev libyaml-dev

    # build infrastructure
    aptitude install python-virtualenv rubygems
    gem install fpm

    fpm --version
    1.4.0

Add workbench user::

    useradd --create-home --shell /bin/bash workbench
    su - workbench


Build package
=============

Get hold of the repository
--------------------------
Initially::

    ssh workbench@oasis.cicer.de
    mkdir -p isarengineering
    git clone git@git.elmyra.de:isarengineering/kotori.git ~/.isarengineering/kotori
    cd isarengineering/kotori

Then::

    ssh workbench@oasis.cicer.de
    cd isarengineering/kotori
    git pull


Build and publish package
-------------------------
The version is taken from ``setup.py``::

    time make deb


Test the package
================

Setup
-----
::

    wget https://packages.elmyra.de/hiveeyes/debian/kotori_0.5.1-1_amd64.deb
    dpkg --install kotori_0.5.1-1_amd64.deb


Troubleshooting
---------------

/var/log/syslog::

    Jan 28 21:36:13 oasis systemd[1]: Starting Kotori data acquisition and graphing toolkit...
    Jan 28 21:36:13 oasis systemd[1]: kotori.service start request repeated too quickly, refusing to start.
    Jan 28 21:36:13 oasis systemd[1]: Failed to start Kotori data acquisition and graphing toolkit.
    Jan 28 21:36:13 oasis systemd[1]: Unit kotori.service entered failed state.

/var/log/kotori/kotori.log::

    pkg_resources.DistributionNotFound: The 'cryptography>=0.7' distribution was not found and is required by pyOpenSSL
