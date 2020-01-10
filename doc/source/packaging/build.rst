.. include:: ../_resources.rst

.. _kotori-build:

############
Build Kotori
############

.. highlight:: bash


*****
Intro
*****
This documentation section describes how to build Kotori Debian packages.
Please find guidelines for setting up the buildhost at :ref:`kotori-buildhost`.


*************
Release steps
*************

Get the source
==============

Get hold of the repository
--------------------------
Initially::

    ssh workbench@buildhost.example.org
    mkdir -p develop
    git clone https://github.com/daq-tools/kotori.git ~/develop/kotori
    cd develop/kotori

Update the repository
---------------------
::

    ssh workbench@buildhost.example.org
    cd develop/kotori
    git pull


Build package
=============
Build Debian package and upload to the package server ``/incoming`` directory, the package version is taken from ``setup.py``::

    # build debian package for regular daq flavor (28 MB)
    make debian-package flavor=daq

    # build debian package for advanced daq flavor
    # capable of decoding binary messages (38 MB)
    make debian-package flavor=daq-binary

After doing so, the package should appear at https://packages.elmyra.de/elmyra/foss/debian/incoming/.

Build Python sdist egg and publish to egg server::

    make python-package


Publish package
===============
::

    ssh workbench@packages.example.org

    export APTLY_CONFIG=/srv/packages/organizations/elmyra/foss/aptly/aptly.conf
    export APTLY_REPOSITORY=stretch-main
    export APTLY_DISTRIBUTION=stretch
    export PACKAGES_INCOMING=/srv/packages/organizations/elmyra/foss/aptly/public/incoming

    # Add packages to repository
    aptly repo add -config=$APTLY_CONFIG -remove-files=true $APTLY_REPOSITORY $PACKAGES_INCOMING/kotori*.deb

    # Publish repository
    aptly publish update -config=$APTLY_CONFIG -gpg-key=2543A838 -passphrase=esp $APTLY_DISTRIBUTION



Use the package
===============
How to setup the :ref:`kotori-setup`.



----



********
Appendix
********

.. _kotori-buildhost:

Prepare buildhost
=================
Install packages::

    apt-get install aptitude
    aptitude update && aptitude upgrade

    # system
    aptitude install -y fail2ban

    # development
    aptitude install -y git

    # build foundation and header files
    aptitude install -y build-essential python-dev libssl-dev libffi-dev libyaml-dev python-virtualenv

    # build infrastructure
    aptitude install -y python-setuptools

    # scipy, numpy, matplotlib and PyTables
    aptitude install -y pkg-config gfortran libatlas-dev libopenblas-dev liblapack-dev libhdf5-dev libnetcdf-dev liblzo2-dev libbz2-dev
    aptitude install -y libpng12-dev libfreetype6-dev


Install Ruby and RubyGems::

    aptitude install -y ruby2.1 ruby2.1-dev
    ln -s /usr/bin/ruby2.1 /usr/bin/ruby

    ruby --version
    # ruby 2.1.5p273 (2014-11-13) [x86_64-linux-gnu]
    # ruby 2.1.5p273 (2014-11-13) [arm-linux-gnueabihf]

    mkdir install; cd install
    wget https://rubygems.org/rubygems/rubygems-2.6.4.tgz
    tar -xzf rubygems-2.6.4.tgz
    ruby setup.rb

    ln -s /usr/bin/gem2.1 /usr/bin/gem

    gem --version
    2.6.4

Install fpm::

    gem install fpm

    fpm --version
    1.5.0


Add workbench user::

    useradd --create-home --shell /bin/bash workbench
    su - workbench


Current infrastructure
======================
- The designated Debian buildhost is ``oasis.cicer.de``.
- The designated public Debian repository host is ``pulp.cicer.de``.
- Both are running a recent stable Debian distribution, currently Debian Jessie (8.4).

