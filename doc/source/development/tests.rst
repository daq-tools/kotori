#################
Integration tests
#################

*****
About
*****
The tests are mostly full integration tests. They are testing the whole system
and the interactions between the subsystems.

The test suite will assume running instances of Mosquitto, Grafana, InfluxDB and
MongoDB and fire up an in-process instance of Kotori to complement these.

Then, messages are published to the MQTT bus by shelling out to ``mosquitto_pub``.
After that, InfluxDB will be checked to contain the right data and Grafana will
be checked to be accurately provisioned.

While the shellout can well be optimized for efficiency, it is also pleasant
to have a full scenario using regular command line tools covered here.


*****
Setup
*****
::

    make dev-virtualenv


***
Run
***
::

    make test

or::

    make pytest
    make nosetest

or run specific tests with maximum verbosity::

    export PYTEST_OPTIONS="--verbose --verbose --log-level DEBUG --log-cli-level DEBUG --capture=no"

    # Run tests starting with "test_tasmota".
    pytest test ${PYTEST_OPTIONS} -k test_tasmota

    # Run tests marked with "mqtt".
    pytest test ${PYTEST_OPTIONS} -m mqtt

    # Run tests marked with "tasmota", "homie" or "airrohr".
    pytest test ${PYTEST_OPTIONS} -m 'tasmota or homie or airrohr'


To see available markers, type::

    pytest --markers
