#################
Integration tests
#################

*****
About
*****
The tests are mostly full integration tests. They are testing the whole system
and the interactions between the subsystems. That is, the test suite will assume
running instances of Mosquitto, InfluxDB and Grafana and fire up an in-process
instance of Kotori to complement these.

Then, messages are published to the MQTT bus by shelling out to ``mosquitto_pub``.
After that, InfluxDB will be checked to contain the right data and Grafana will
be checked to be provisoned accurately.

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

or run a specific test with maximum verbosity::

    pytest test -k test_tasmota --verbose --log-level DEBUG --log-cli-level DEBUG --capture=no
