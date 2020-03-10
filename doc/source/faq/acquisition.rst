.. include:: ../_resources.rst

.. _data-acquisition-in-a-nutshell:

##############################
Data acquisition in a nutshell
##############################


********
Question
********
    - I am seeing lots of things about MQTT_. How is the data actually imported into InfluxDB_?
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

- `Data acquisition using MQTT <https://getkotori.org/docs/handbook/acquisition/protocol/mqtt.html>`_
- `Data acquisition using HTTP <https://getkotori.org/docs/handbook/acquisition/protocol/http.html>`_
