.. include:: ../../../_resources.rst

.. _daq-arduino:

#############################
Data acquisition with Arduino
#############################

.. todo:: Add complete example for Arduino.

.. _json-arduino:

*******************
Use JSON on Arduino
*******************
.. highlight:: cpp

`Arduino JSON library`_, an elegant and efficient JSON library for embedded systems::


    // Prepare data, build JSON object

    StaticJsonBuffer<256> jsonBuffer;

    JsonObject& root = jsonBuffer.createObject();
    root["weight"]      = 84.84f;
    root["humidity"]    = 60.08f;
    root["temperature"] = 28.90f;

    // Debugging
    root.printTo(Serial);

    // Serialize data
    char payload[256];
    root.printTo(payload, sizeof(payload));

    // This will print:
    // {"weight":84.84,"humidity":60.08,"temperature":28.90}


.. _json-homie:

************************
Transmit data from Homie
************************
.. highlight:: cpp

Homie_ is an MQTT convention for the IoT. `homie-esp8266`_ is the corresponding ESP8266 framework implementation.
This section tries to give a short introduction about how to publish
telemetry data from a Homie-based firmware in JSON format to the MQTT bus.

1. Use a configuration like::

    {
        "name": "slartibartfast",
        "device_id": "node-1",
        "wifi": {
            "ssid": "Network_1",
            "password": "I'm a Wi-Fi password!"
        },
        "mqtt": {
            "host": "kotori.example.net",
            "port": 1883,
            "base_topic": "mqttkit-1/testdrive/area-42/"
        }
    }

.. note::

    Especially have a look at the parameters ``base_topic`` and ``device_id``:
    They make up the prefix parts of an appropriate MQTT topic string.
    See also :ref:`daq-mqtt` for general information about MQTT telemetry data publishing.

2. Use code like::

    HomieNode jsonNode("data", "__json__");
    jsonNode.setProperty("__json__").setRetained(false).send(payload);

.. note::

    This will make up the suffix part ``data/__json__`` of an
    appropriate recognized MQTT topic string.

