#############
Project tasks
#############


************
Introduction
************

This directory contains common tasks used for project maintenance. Mostly, it
contains tasks related to release package and image building.

To get an overview about the implemented tasks, invoke::

    invoke --list


*********
Packaging
*********

Tasks for building distribution packages and images using Docker. Building
packages and images is a three-stage process:

1. Build Docker baseline images.
2. Build distribution packages using those baseline images.
3. Build Docker images using those packages.
4. Run basic tests on Docker images.
