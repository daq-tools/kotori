.. include:: ../_resources.rst

.. _daq-arduino:
.. _daq-arduino-esp8266:

#####################
C++ (Arduino/ESP8266)
#####################

************
Introduction
************
This example will send JSON over MQTT over WiFi - on Arduino Core for ESP8266.


*************
Prerequisites
*************
- `Arduino JSON library`_, an elegant and efficient JSON library for embedded systems.
- `Adafruit MQTT Library`_, an Arduino library for MQTT support.

.. _Adafruit MQTT Library: https://github.com/adafruit/Adafruit_MQTT_Library


*******
Example
*******

.. highlight:: cpp

::

    #include <ESP8266WiFi.h>
    #include <ArduinoJson.h>
    #include "Adafruit_MQTT.h"
    #include "Adafruit_MQTT_Client.h"

    // WLAN credentials.
    #define WIFI_SSID     = "SSID";
    #define WIFI_PASSWORD = "PASS";


    // The address of the MQTT broker to connect to.
    #define MQTT_BROKER         "daq.example.org"
    #define MQTT_PORT           1883

    // A MQTT client ID, which should be unique across multiple devices for a user.
    // Change some 8 bytes of random hex-value here!
    #define MQTT_CLIENT_ID      "ef3423be2"

    // The MQTT topic to transmit sensor readings to.
    #define MQTT_TOPIC          "mqttkit-1/foo/bar/1/data.json"

    // The credentials to authenticate with the MQTT broker.
    #define MQTT_USERNAME       ""
    #define MQTT_PASSWORD       ""

    // How often to retry connecting to the MQTT broker.
    #define MQTT_RETRY_COUNT    5

    // How long to delay between MQTT (re)connection attempts (seconds).
    #define MQTT_RETRY_DELAY    1.5f


    // Connect to WiFi.
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    Serial.print(" ");
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.printf(".");
    }
    Serial.printf(" got IP-address ");
    Serial.println("[wifi] connected");
    // Printing the ESP IP address
    Serial.print(WiFi.localIP());


    // Create an ESP8266 WiFiClient object to connect to the MQTT server.
    WiFiClient wifi_client;

    // Setup the MQTT client class by passing in the WiFi client and MQTT server and login details.
    Adafruit_MQTT_Client mqtt(&wifi_client, MQTT_BROKER, MQTT_PORT, MQTT_CLIENT_ID, MQTT_USERNAME, MQTT_PASSWORD);

    // Setup MQTT publishing handler.
    Adafruit_MQTT_Publish mqtt_publisher = Adafruit_MQTT_Publish(&mqtt, MQTT_TOPIC);

    // Connect to the MQTT broker.
    mqtt.connect();


    // Prepare data, build JSON object.
    StaticJsonBuffer<256> jsonBuffer;
    JsonObject& root    = jsonBuffer.createObject();
    root["weight"]      = 84.84f;
    root["humidity"]    = 60.08f;
    root["temperature"] = 28.90f;

    // Debugging.
    //root.printTo(Serial);
    // This will print:
    // {"weight":84.84,"humidity":60.08,"temperature":28.90}

    // Serialize data.
    char payload[256];
    root.printTo(payload, sizeof(payload));

    // Publish data.
    if (mqtt_publisher.publish(payload)) {
        Serial.println("success.");
    } else {
        Serial.println("fail.");
    }


*****************
Real applications
*****************
- The ESP8266-based sensor node firmware `node-wifi-mqtt.ino`_ of the `Hiveeyes project`_, see
  `Basic WiFi/MQTT sensor node <https://hiveeyes.org/docs/arduino/firmware/node-wifi-mqtt/README.html>`_.
- Autonome Zelle - Solar-Feinstaub-Wetter-Vergleichsding
    - https://git.cicer.de/autonome-zelle/autonome-zelle-sfwv
    - https://community.hiveeyes.org/t/versuchsaufbau-autonome-zelle-solar-feinstaub-wetter-vergleichsding/1373
