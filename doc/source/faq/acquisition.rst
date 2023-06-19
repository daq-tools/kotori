.. include:: ../_resources.rst

.. _data-acquisition-in-a-nutshell:

##############################
Data acquisition in a nutshell
##############################


********
Question
********
- I am seeing lots of things about MQTT_. How is the data actually imported into the database?
- Is data acquisition also possible through HTTP POST requests to the defined topic / channel address?


******
Answer
******
Data is usually ingested through MQTT_ [1]. However, ingesting data using HTTP [2]
is also possible by adding a configuration object like outlined within
:ref:`forward-http-to-mqtt`.


*******
Details
*******
A minimal example of how to publish data using MQTT is::

    mosquitto_pub -h localhost -t mqttkit-1/testdrive/area-42/node-1/data/temperature -m '42.84'

A minimal example of how to submit data using HTTP is::

    http POST http://localhost:24642/api/mqttkit-1/testdrive/area-42/node-1/data temperature:=42.84


*********
Resources
*********
Please follow the documentation to read more details about data acquisition through MQTT and HTTP.

- :ref:`Data acquisition using MQTT <daq-mqtt>` for transmitting
  telemetry data over MQTT from other environments (Python, Arduino, mbed).
- :ref:`Data acquisition using HTTP <daq-http>` for transmitting
  telemetry data over HTTP.


********
Examples
********
- See :ref:`basic-mqtt-example` for submitting measurement values /
  telemetry data from the command line.

- For sending a simple oscillating signal to Kotori from the command line,
  please have a look at the :ref:`sawtooth-signal` page.
