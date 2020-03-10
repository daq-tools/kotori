.. include:: ../_resources.rst

.. _daq-lua-nodemcu:

#############
Lua (NodeMCU)
#############

.. highlight:: lua


************
Introduction
************
This example will send JSON over MQTT over WiFi - on Lua for NodeMCU.


.. contents::
   :local:
   :depth: 1

----

.. _daq-lua-nodemcu-mqtt:

****
MQTT
****

Prerequisites
=============
- https://nodemcu.readthedocs.io/en/dev-esp32/modules/mqtt/


Synopsis
========
::

    -- WLAN credentials.
    WIFI_SSID     = "SSID"
    WIFI_PASSWORD = "PASS"

    -- The address of the MQTT broker to connect to.
    MQTT_BROKER_HOST = "daq.example.org"
    MQTT_BROKER_PORT = 1883

    -- A MQTT client ID, which should be unique across multiple devices for a user.
    -- Change some 8 bytes of random hex-value here!
    MQTT_CLIENT_ID   = "ef3423be2"

    -- The MQTT topic to transmit sensor readings to.
    MQTT_TOPIC       = "mqttkit-1/foo/bar/1/data.json"


    -- Connect to WiFi.
    wifi.mode(wifi.STATION, true)
    wifi.start()
    wifi.sta.config({ssid=WIFI_SSID, pwd=WIFI_PASSWORD, auto=true}, true)

    -- Define telemetry data.
    data = {
        temperature = 42.84,
        humidity = 51.08,
    }

    -- Create JSON payload.
    -- https://nodemcu.readthedocs.io/en/master/modules/sjson/
    print("Creating JSON payload.")
    sjson.encode(data)
    ok, json = pcall(sjson.encode, data)
    if ok then
        print("JSON payload:", json)
    else
        print("ERROR: Encoding to JSON failed!")
        return
    end

    -- Publish data using MQTT.
    m = mqtt.Client(MQTT_CLIENT_ID, 120)
    m:connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 0,
        function(client)
            client:publish(MQTT_TOPIC, json, 1, 0, function(client)
                print("########## Success: MQTT message sent.")
            end)
        end,
        function(client, reason)
            print("########### MQTT connect failed. Reason: " .. reason)
        end
    )



.. _daq-lua-nodemcu-http:

****
HTTP
****

Prerequisites
=============
- https://nodemcu.readthedocs.io/en/dev-esp32/modules/http/


Synopsis
========
::

    -- Define data channel.
    CHANNEL_URI = "https://daq.example.org/api/mqttkit-1/foo/bar/1/data"

    -- Publish data using HTTP.
    headers = {
      ["Content-Type"] = "application/json",
    }
    http.post(CHANNEL_URI, { headers = headers }, json,
      function(code, data)
        if (code < 0) then
          print("HTTP request failed")
        else
          print(code, data)
        end
      end)

    end


*****************
Real applications
*****************
- https://github.com/ISEMS/ISEMS-ESP32/tree/master/LUA/ff-esp32-openmppt
