.. include:: ../../../_resources.rst
.. highlight:: bash

.. _daq-http:

##########################
Data acquisition over HTTP
##########################

.. contents::
   :local:
   :depth: 1


************
Introduction
************
Measurement readings can be acquired through HTTP using different formats
like x-www-form-urlencoded, JSON and CSV.

The former both are *full-qualified* serialization formats containing **named**
sensor readings of key/value pairs, CSV is an *unqualified* serialization format.
*Unqualified* serialization formats require field names to be announced upfront
by sending a special CSV header. See :ref:`daq-http-csv` for an example.

Both single shot readings as well as bulk transfer modes are supported. There is
a special field name ``time`` which is reserved for submitting data readings
including timestamps. This is specifically important for bulk data submissions,
see :ref:`daq-http-with-timestamp` for an example and the whole list of
available :ref:`daq-timestamp-formats` as reference.

.. seealso:: :ref:`Transmit a periodic sawtooth signal over HTTP <sawtooth-http>`


*****
Setup
*****
HTTP data acquisition works using a HTTP-to-MQTT convergence handler.
Please have a look at :ref:`forward-http-to-mqtt` about how to configure
a HTTP endpoint as an addon to a :ref:`application-mqttkit` application.


**************
Basic examples
**************


.. _daq-curl:

Data acquisition with curl
==========================
A basic example about sending telemetry data using ``curl``::

    # Define channel address
    export DEVICE_REALM="mqttkit-1"
    export DEVICE_TOPIC="testdrive/area-42/node-1"

    # Compute HTTP URI
    export HTTP_URI=http://localhost:24642/api/$DEVICE_REALM/$DEVICE_TOPIC/data

    # Send readings in JSON format
    echo '{"temperature": 42.84, "humidity": 83}' | curl --request POST --header 'Content-Type: application/json' --data @- $HTTP_URI

    # Send readings in x-www-form-urlencoded format
    echo 'temperature=42.84&humidity=83' | curl --request POST --header 'Content-Type: application/x-www-form-urlencoded' --data @- $HTTP_URI


.. _daq-httpie:

.. _daq-python-httpie:

Data acquisition with HTTPie
============================
HTTPie_ is a cURL-like tool for humans and even more convenient.

Setup
=====
Choose one of these ways to install HTTPie_, depending on your platform::

    # Debian/Ubuntu
    apt install httpie

    # Macports
    port install httpie

    # Vanilla Python
    pip install httpie

    # Windows
    # Install the Chocolatey package manager: https://chocolatey.org/install
    cinst httpie -source python


Single readings
===============
::

    # Send readings in JSON format
    http POST http://localhost:24642/api/mqttkit-1/testdrive/area-42/node-1/data temperature:=42.84 humidity:=83

    # Send readings in x-www-form-urlencoded format
    http --form POST http://localhost:24642/api/mqttkit-1/testdrive/area-42/node-1/data temperature:=42.84 humidity:=83


.. _daq-http-with-timestamp:

Readings with timestamp
=======================
When sending data readings using JSON or x-www-form-urlencoded, a timestamp may be supplied.
Example::

    # Send readings with human-readable timestamp in UTC
    http POST http://localhost:24642/api/mqttkit-1/testdrive/area-42/node-1/data time=2016-12-07T17:30:15.842428Z temperature:=42.84 humidity:=83

See also the whole list of :ref:`daq-timestamp-formats`.


.. _daq-http-annotation:

Annotations
===========
`Grafana Annotations`_ can be created through the HTTP interface at the ``/event`` endpoint.
While arbitrary fields can be submitted, Grafana_ evaluates the fields ``title``, ``text`` and ``tags``.
It is possible to use HTML inside the ``text`` field, for example to link this event to another web application.

The synopsis is::

    http POST http://localhost:24642/api/mqttkit-1/testdrive/area-42/node-1/event title='Some event' text='<a href="https://somewhere.example.org/events?reference=482a38ce-791e-11e6-b152-7cd1c55000be">see also</a>' tags='event,alert,important' reference='482a38ce-791e-11e6-b152-7cd1c55000be'

Annotations can also be submitted retroactively, just add a ``time`` field::

    http POST http://localhost:24642/api/mqttkit-1/testdrive/area-42/node-1/event time=2016-12-07T17:30:15.842428Z title='Some event in the past'

See also the whole list of :ref:`daq-timestamp-formats`.


.. _daq-http-csv:

**********
CSV format
**********
CSV is an universal but *unqualified* serialization format, so field names
have to be announced upfront by sending a special CSV header.

These registered field names are retained across server restarts and will
be mapped against the value-only readings before propagating them to the
storage subsystem and other downstream data channels.
The list of registered field names can be updated any time.


Single readings
===============
Transmit a single reading using CSV serialization.
To register field names with a data channel before sending any sensor readings,
use a comma separated list of field names prefixed by ``##``
as the data line format, e.g. ``## weight, temperature, humidity``.

Example::

    # 1. Send field names once
    echo '## weight, temperature, humidity' | http POST http://localhost:24642/api/mqttkit-1/testdrive/area-42/node-1/data Content-Type:text/csv

    # 2. Send readings
    echo '42.42, 34.02, 82.82' | http POST http://localhost:24642/api/mqttkit-1/testdrive/area-42/node-1/data Content-Type:text/csv

.. note:: The line format is whitespace agnostic.


Readings with timestamp
=======================
When sending data readings using CSV, a timestamp may be supplied.
Examples::

    # 1. Send field names
    echo '## time, weight, temperature, humidity' | http POST http://localhost:24642/api/mqttkit-1/testdrive/area-42/node-1/data Content-Type:text/csv

    # 2.a Send readings with human-readable timestamp in UTC
    echo '2016-12-07T17:00:00.842428Z, 50.42,40.02,82.82' | http POST http://localhost:24642/api/mqttkit-1/testdrive/area-42/node-1/data Content-Type:text/csv

    # 2.b Send readings with timestamp in nanoseconds since Epoch
    echo '1478021421000000000, 50.42,40.02,82.82' | http POST http://localhost:24642/api/mqttkit-1/testdrive/area-42/node-1/data Content-Type:text/csv

    # 2.c Sending an empty timestamp will use current server time
    echo ', 50.42,40.02,82.82' | http POST http://localhost:24642/api/mqttkit-1/testdrive/area-42/node-1/data Content-Type:text/csv

See also the whole list of :ref:`daq-timestamp-formats`.


Bulk readings
=============
The field name announcement header and multiple readings can be sent at once for HTTP bulk upload.
Each line should be separated by a newline ``\n``.

Let's assume a file ``data.csv`` containing::

    ## time, weight, temperature, humidity, voltage
    2016-08-14T21:02:06, 58.697, 19.6, 56.1, 4.13
    2016-08-14T21:22:06, 58.663, 19.4, 58.3, 4.13
    2016-08-14T21:42:06, 58.601, 19.1, 57.7, 4.12

Upload the file all at once::

    cat data.csv | http POST http://localhost:24642/api/mqttkit-1/testdrive/area-42/node-1/data Content-Type:text/csv



Open Hive Support
=================
There's some support for proprietary/legacy data formats.
Here, the service understands a custom header format starting with "Datum/Zeit" or "Date/Time", like::

    echo 'Datum/Zeit,Gewicht,Aussen-Temperatur,Aussen-Feuchtigkeit,Spannung' | http POST http://localhost:24642/api/mqttkit-1/testdrive/area-42/node-1/data Content-Type:text/csv

Sensor readings are transmitted using local time.
On further processing, we assume them being in Central European Time (CET).
Example::

    echo '2016/08/14 21:02:06,  58.697, 19.6, 56.1, 4.13' | http POST http://localhost:24642/api/mqttkit-1/testdrive/area-42/node-1/data Content-Type:text/csv

.. tip::

    While this is possible, you should definitively favor using the established conventions, so please:

        - send timestamps using the field name ``time``
        - send timestamps in `ISO 8601`_ format, using UTC


****************************
Periodic acquisition example
****************************

.. _sawtooth-http:

Sawtooth
========
The characteristics of sawtooth signals (dynamic, slowly oscillating)
are convenient to generate measurement sensor readings and publish
telemetry data without having any hardware in place.

Infrastructure
--------------
Let's define the basic infrastructure for hands-free, periodic dry-dock measurements::

    # Connect sensor value readings with telemetry transmitter
    measure() { sensor | transmitter; }

    # A simple main loop ticking once each second
    loop() { while true; do measure; echo -n .; sleep 1; done; }

Sensor
------
Define an example sensor emitting a single sample of a sawtooth signal in JSON format,
using the value of the current second::

    sensor() { echo "{\"second\": $(date +%-S)}"; }

Transmitter
-----------
Define a transmitter based on HTTPie_::

    # Define channel address
    export DEVICE_REALM="mqttkit-1"
    export DEVICE_TOPIC="testdrive/area-42/clockdemo-1"

    # Define transmitter
    transmitter() { http POST http://localhost:24642/api/$DEVICE_REALM/$DEVICE_TOPIC/data; }

Start publishing::

    loop

Result
------
Sawtooth signal made from oscillating value of the current second.

.. raw:: html

    <iframe src="https://swarm.hiveeyes.org/grafana/dashboard-solo/db/clockdemo?panelId=5&from=1464307860728&to=1464308765714" width="100%" height="425" frameborder="0"></iframe>

|clearfix|


*****************
Language bindings
*****************

.. list-table:: List of Kotori HTTP clients
   :widths: 10 40
   :header-rows: 1
   :class: table-generous

   * - Name
     - Description

   * - Python
     - See :ref:`transmit from Python <daq-python-http>` using the fine Requests_ http library.

   * - PHP
     - Visit :ref:`daq-php` for a library and and an example how to transmit telemetry data from PHP.


***************
Troubleshooting
***************
Some guidelines about troubleshooting the HTTP interface when sending invalid data acquisition requests.

Empty request body
==================
Empty request bodies don't make sense::

    http POST http://localhost:24642/api/mqttkit-1/testdrive/area-42/node-1/data Content-Type:text/csv

so the service will reject them appropriately::

    HTTP/1.1 400 Bad Request
    Channel-Id: /mqttkit-1/testdrive/area-42/node-1
    Content-Type: application/json
    Date: Sat, 10 Dec 2016 19:16:44 GMT

    [
        {
            "message": "Empty request body",
            "type": "error"
        }
    ]

Invalid content type
====================
The HTTP interface currently accepts the media types:

    - ``application/json``
    - ``application/x-www-form-urlencoded``
    - ``text/csv``

Sending content designated with an invalid media type, e.g. ``unknown/format``::

    echo '58.697, 19.6, 56.1, 4.13' | http POST http://localhost:24642/api/mqttkit-1/testdrive/area-42/node-1/data Content-Type:unknown/format

will also get rejected::

    HTTP/1.1 415 Unsupported Media Type
    Channel-Id: /mqttkit-1/testdrive/area-42/node-1
    Content-Type: application/json
    Date: Sat, 10 Dec 2016 19:17:08 GMT

    [
        {
            "message": "Unable to handle Content-Type 'unknown/format'",
            "type": "error"
        }
    ]

Readings without fields
=======================
When using unqualified data serialization formats like CSV, field names must
have been registered prior to sending sensor readings. When not doing so::

    echo -e '2016-12-07T18:30:15+0100,  58.697, 19.6, 56.1, 4.13' | http POST http://localhost:24642/api/mqttkit-1/testdrive/area-42/node-unknown/data Content-Type:text/csv

the service will respond::

    HTTP/1.1 400 Bad Request
    Channel-Id: /mqttkit-1/testdrive/area-42/node-1
    Content-Type: application/json
    Date: Sat, 10 Dec 2016 19:17:25 GMT

    [
        {
            "message": "Could not process data, please supply field names before sending readings",
            "type": "error"
        }
    ]

