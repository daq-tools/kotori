.. include:: ../../_resources.rst


.. _error-signalling:

################
Error signalling
################
.. highlight:: bash


************
Introduction
************
When receiving invalid payloads on data acquisition, errors will be signalled over MQTT.
If you are sending data to the system and it is not arriving as expected, please make sure
to listen to error signals on MQTT topics corresponding to your data channel to find out about
the reason.

So, if your data channel would be::

    mqttkit-1/testdrive/area-42/node-1/data.json

the corresponding error signalling channel would be::

    mqttkit-1/testdrive/area-42/node-1/error.json


********
Examples
********

JSON format error
=================
While listening on the MQTT bus::

    mosquitto_sub -h kotori.example.org -t "mqttkit-1/#" -v

and sending an invalid formatted JSON message like::

    echo '{"value": 42.42' | mosquitto_pub -h kotori.example.org -t mqttkit-1/testdrive/area-42/node-1/data.json -l

the system will respond with a MQTT "response" on the corresponding topic with suffix ``error.json``::

    mqttkit-1/testdrive/area-42/node-1/error.json {
        "message": "Expecting object: line 1 column 14 (char 13)",
        "type": "<type 'exceptions.ValueError'>",
        "description": "Error processing MQTT message \"{\"value\": 42.42\" from topic \"mqttkit-1/testdrive/area-42/node-1/data.json\"."
    }

Database error
==============
When sending a payload with an existing field already seeded in a different data type::

    echo '{"value": "invalid"}' | mosquitto_pub -h kotori.example.org -t mqttkit-1/testdrive/area-42/node-1/data.json -l

the system will respond with::

    mqttkit-1/testdrive/area-42/node-1/error.json {
        "message": "400: {\"error\":\"field type conflict: input field \\\"value\\\" on measurement \\\"area_42_node_1_sensors\\\" is type string, already exists as type float dropped=1\"}\n",
        "type": "<class 'influxdb.exceptions.InfluxDBClientError'>",
        "description": "Error processing MQTT message \"{\"value\": \"invalid\"}\" from topic \"mqttkit-1/testdrive/area-42/node-1/data.json\"."
    }

HTTP acquisition
================
The system is currently just capable to send error signals over MQTT. So after provisioning a CSV channel like::

    echo '## time,value' | http POST http://kotori.example.org/api/mqttkit-1/testdrive/area-42/node-1/data Content-Type:text/csv
    echo '2017-05-01 22:39:09,42.42' | http POST http://kotori.example.org/api/mqttkit-1/testdrive/area-42/node-1/data Content-Type:text/csv

and then sending an invalid payload like::

    echo '2017-05-01 22:39:09,invalid' | http POST http://kotori.example.org/api/mqttkit-1/testdrive/area-42/node-1/data Content-Type:text/csv

The system will also respond over MQTT with::

    mqttkit-1/testdrive/area-42/node-1/error.json {
        "message": "400: {\"error\":\"field type conflict: input field \\\"value\\\" on measurement \\\"area_42_node_1_sensors\\\" is type string, already exists as type float dropped=1\"}\n",
        "type": "<class 'influxdb.exceptions.InfluxDBClientError'>",
        "description": "Error processing MQTT message \"{\"time\": \"2017-05-01 22:40:09\", \"value\": \"invalid\"}\" from topic \"mqttkit-1/testdrive/area-42/node-1/data.json\"."
    }

