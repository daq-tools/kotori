.. include:: ../_resources.rst

.. _daq-micropython:

###########
MicroPython
###########

.. highlight:: python


.. _daq-micropython-mqtt:

****
MQTT
****

Prerequisites
=============
- https://github.com/micropython/micropython-lib/blob/master/micropython/umqtt.simple/umqtt/simple.py


Synopsis
========
::

    import json

    # MicroPython MQTT library.
    from umqtt.simple import MQTTClient

    # Define data channel.
    channel_broker = "daq.example.org"
    channel_port = 1883
    channel_topic = "https://daq.example.org/api/mqttkit-1/foo/bar/1/data"

    # Prepare data payload.
    data = {"temperature": 42.84, "humidity": 83.3}
    payload = json.dumps(data)

    # Submit using MQTT.
    client = MQTTClient("ef3423be2", channel_broker, port=channel_port, keepalive=6)
    client.connect()
    client.publish(channel_topic, payload)
    client.disconnect()




.. _daq-micropython-http:

****
HTTP
****

Prerequisites
=============
- https://github.com/micropython/micropython-lib/blob/master/python-ecosys/urequests/urequests.py

Synopsis
========
::

    import urequests

    # Define data channel.
    channel_uri = "https://daq.example.org/api/mqttkit-1/foo/bar/1/data"

    # Prepare data payload.
    data = {"temperature": 42.84, "humidity": 83.3}
    payload = json.dumps(data)

    # Submit using HTTP.
    response = urequests.post(channel_uri, data=payload, headers={"Content-Type": "application/json"})
    if response.status_code in [200, 201]:
        return True
    else:
        raise Exception("Telemetry failed")


*****************
Real applications
*****************
- https://git.cicer.de/autonome-zelle/fipy-nbiot-rtd
- https://github.com/hiveeyes/terkin-datalogger
