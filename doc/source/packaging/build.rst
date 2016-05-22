.. include:: ../_resources.rst

.. _kotori-build:

###############
Kotori building
###############

The designated Debian buildslave is ``oasis.cicer.de``. It is currently running Debian Jessie (8.4).
Please find guidelines for setting up the buildslave at :ref:`kotori-buildslave`.

*****
Steps
*****

Build package
=============

Get hold of the repository
--------------------------
Initially::

    ssh workbench@oasis.cicer.de
    mkdir -p isarengineering
    git clone git@git.elmyra.de:isarengineering/kotori.git ~/isarengineering/kotori
    cd isarengineering/kotori

Then::

    ssh workbench@oasis.cicer.de
    cd isarengineering/kotori
    git pull


Cut release, build and publish package
--------------------------------------
See :ref:`kotori-release`.


Use the package
===============
How to setup the :ref:`kotori-setup`.


********
Appendix
********

.. _kotori-buildslave:

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

