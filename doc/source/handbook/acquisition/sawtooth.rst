.. include:: ../../_resources.rst

.. _sawtooth-signal:

###############
Sawtooth signal
###############
.. highlight:: bash

The characteristics of sawtooth signals (dynamic, slowly oscillating)
are convenient to generate and publish measurement or telemetry data
values without having any hardware in place.

There are different means of transmitting a sawtooth signal to Kotori:

.. contents::
   :local:
   :depth: 1

----

.. _sawtooth-mqtt:

.. _sawtooth-bash:

****
MQTT
****

The following examples depend on ``mosquitto_pub`` usually contained
in the ``mosquitto-clients`` distribution package or similar::

    # Setup "mosquitto_pub"
    aptitude install mosquitto-clients


Single sawtooth signal
======================

Sensor
------
Let's define a an example sensor emitting a single sawtooth signal::

    # Define an example sensor emitting a single sample of a sawtooth signal in JSON format
    sensor() { echo "{\"sawtooth\": $(date +%-S)}"; }

Check if the sensor works properly::

    # Read sensor value
    sensor
    {"sawtooth": 42}

    # Verify it's actually JSON
    sensor | python -mjson.tool
    {
        "sawtooth": 42
    }


Transmitter
-----------
Get real and actually transmit sensor values to Kotori by publishing them to the MQTT bus::

    # Where to send data to
    export MQTT_BROKER=kotori.example.org
    export MQTT_TOPIC=mqttkit-1/testdrive/area-42/node-1

    # Define the transmission command to send telemetry data to the "testdrive" network
    transmitter() { mosquitto_pub -h $MQTT_BROKER -t $MQTT_TOPIC/message-json -l; }

    # Acquire and transmit a single sensor reading
    sensor | transmitter


Periodic transmitter
--------------------
"hands-free", periodic dry-dock measurements::

    measure() { sensor | transmitter; }
    loop() { while true; do measure; echo -n .; sleep 1; done; }

Start publishing::

    loop

Result:

.. raw:: html

    <iframe src="https://swarm.hiveeyes.org/grafana/dashboard-solo/db/clockdemo?panelId=5&from=1464307860728&to=1464308765714" width="100%" height="425" frameborder="0"></iframe>

.. container:: width-800

    Sawtooth signal made from oscillating value of current second.

|clearfix|

In ``/var/log/kotori/kotori.log``, you should see things like::

    2016-05-27T03:03:58+0200 [kotori.daq.services.mig            ] INFO: [mqttkit-1   ] transactions: 1.00 tps


Multiple sawtooth signals
=========================
A more advanced sensor might be::

    # Let's define multiple sawtooth signals, also derived from current time
    sensor() { jo second=$(date +%-S) minute=$(date +%-M) hour=$(date +%-H) day=$(date +%-d) month=$(date +%-m); }

Check if the sensor works properly::

    # Read sensor values
    sensor | python -mjson.tool
    {
        "day": 27,
        "hour": 2,
        "minute": 37,
        "month": 5,
        "second": 45
    }

Restart transmitting::

    loop

Result:

.. highlight:: bash

.. raw:: html

    <iframe src="https://swarm.hiveeyes.org/grafana/dashboard-solo/db/clockdemo?panelId=8&from=20160527T002500&to=20160527T013000" width="100%" height="425" frameborder="0"></iframe>

.. container:: width-800

    Whole date of second, minute, hour, day and month.

|clearfix|

.. note::

    This uses the great ``jo`` tool by `Jan-Piet Mens`_ to format a JSON message on the command line, see also:

        - http://jpmens.net/2016/03/05/a-shell-command-to-create-json-jo/
        - https://github.com/jpmens/jo

    There are source release archives and windows binaries:

        - https://github.com/jpmens/jo/releases

    as well as distribution packages for Debian-based systems, e.g.:

        - https://launchpad.net/~duggan/+archive/ubuntu/jo/+build/9339941/+files/jo_1.0+1~ubuntu12.04.1_i386.deb
        - https://launchpad.net/~duggan/+archive/ubuntu/jo/+build/9339940/+files/jo_1.0+1~ubuntu12.04.1_amd64.deb


.. _sawtooth-http:

.. _sawtooth-curl:

****
HTTP
****

.. tip::

    For making Kotori listen to HTTP requests for telemetry data acquisition,
    please have a look at :ref:`forward-http-to-mqtt` about how to configure
    a HTTP endpoint for your :ref:`application-mqttkit` application
    and see :ref:`daq-http` for transmitting telemetry data over HTTP from
    different environments.


Single sawtooth signal
======================

Sensor
------
Let's use one of the sensor definitions from above.


curl transmitter
----------------
Get real and publish sensor values to the MQTT bus::

    # Where to send data to
    export HTTP_URI=http://kotori.example.org

    # Redefine transmitter to use HTTP instead of MQTT
    transmitter() { curl --request POST --header 'Content-Type: application/json' --data @- $HTTP_URI/api/$MQTT_TOPIC/data; echo; }

Restart transmitting::

    loop


HTTPie transmitter
------------------
When using HTTPie_, the transmitter command is even more compact::

    # Redefine transmitter to use HTTPie instead of curl
    transmitter() { http POST $HTTP_URI/api/$MQTT_TOPIC/data; }

Restart transmitting::

    loop

