#################
Integration tests
#################


*****
About
*****

The tests are mostly full integration tests. They are testing the whole system
and the interactions between the subsystems.

Messages will get published to the MQTT bus by shelling out to ``mosquitto_pub``.
After that, the database will be checked to contain the right data and Grafana will
be checked to be accurately provisioned.

While the shell-out can well be optimized for efficiency, it is also pleasant
to have a full scenario using regular command line tools covered here.


*************
Prerequisites
*************

Environment
===========

Install some needed packages::

    apt-get install python3-venv python3-dev docker-compose mosquitto-clients

Foundation services
===================

The test suite will assume running instances of Mosquitto, CrateDB, InfluxDB, MongoDB
and Grafana and fire up an in-process instance of Kotori to complement these. Please
have a look at :ref:`setup-docker` in order to get the complementing services
up and running in a quick and ad hoc manner.

Run Mosquitto, CrateDB, InfluxDB, MongoDB and Grafana as Docker containers::

    make start-foundation-services


***
Run
***

Run all tests::

    make test

Run specific tests with maximum verbosity::

    export PYTEST_OPTIONS="--verbosity=3 --log-level DEBUG --log-cli-level DEBUG --capture=no"

    # Run tests starting with "test_tasmota".
    pytest test ${PYTEST_OPTIONS} -k test_tasmota

    # Run tests marked with "mqtt".
    pytest test ${PYTEST_OPTIONS} -m mqtt

    # Run tests marked with "tasmota", "homie" or "airrohr".
    pytest test ${PYTEST_OPTIONS} -m 'tasmota or homie or airrohr'

    # Run tests with CrateDB as database backend.
    pytest test ${PYTEST_OPTIONS} -m cratedb

To see available markers, type::

    pytest --markers
