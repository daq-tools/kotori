.. include:: ../../../_resources.rst

.. _daq-python:

######
Python
######

.. contents::
   :local:
   :depth: 1

----

.. _daq-python-mqtt:

****
MQTT
****

Setup
=====
.. highlight:: bash

Install `paho-mqtt`_, the MQTT Python client library from the `Eclipse Paho`_ project.
Choose one of these methods::

    # Vanilla Python
    pip install paho-mqtt

    # Macports
    port install py-paho-mqtt


Transmit
========
.. highlight:: python

A basic example for publishing sensor readings to MQTT::

    import paho.mqtt.client as mqtt

    # -------------------------------
    #  A. Where to send measurements
    # -------------------------------

    # MQTT broker host
    mqtt_broker = 'localhost'

    # MQTT bus topic
    mqtt_topic = u'{realm}/{network}/{gateway}/{node}/data.json'.format(
        realm   = 'mqttkit-1',
        network = 'ea2a38ce-791e-11e6-b152-7cd1c38000be',
        gateway = 'clar14',
        node    = '1'
    )

    # --------------------
    #  B. Example reading
    # --------------------
    measurement = {
        'temp-inside':  33.33,
        'temp-outside': 42.42,
        'hum-inside':   79.12,
        'hum-outside':  83.34
    }

    # --------------------
    #  C. Publish reading
    # --------------------

    # Serialize data as JSON
    payload = json.dumps(measurement)

    # Publish to MQTT
    pid = os.getpid()
    client_id = '{}:{}'.format('client', str(pid))
    backend = mqtt.Client(client_id=client_id, clean_session=True)
    backend.connect(mqtt_broker)
    backend.publish(mqtt_topic, payload)
    backend.disconnect()



.. _daq-python-http:
.. _daq-python-requests:

****
HTTP
****

Setup
=====
.. highlight:: bash

Choose one of these for installing Requests_::

    # Vanilla Python
    pip install requests

    # Debian
    aptitude install python-requests

    # Macports
    port install py-requests


Transmit
========
.. highlight:: python

Basic examples::

    import requests

    # Define an example sensor reading
    data = {"temperature": 42.84, "humidity": 83}

    # Transmit using JSON (application/json)
    requests.post("http://localhost:24642/api/mqttkit-1/testdrive/area-42/node-1/data", json=data).json()

    # Transmit as regular HTTP POST (application/x-www-form-urlencoded)
    requests.post("http://localhost:24642/api/mqttkit-1/testdrive/area-42/node-1/data", data=data).json()

CSV Format
==========
::

    # Define URI
    uri = "http://localhost:24642/api/mqttkit-1/testdrive/area-42/node-1/data"

    # 1. Send field names
    requests.post(uri, data="## weight, temperature, humidity, voltage", headers={'Content-Type': 'text/csv'}).json()

    # 2. Send readings
    requests.post(uri, data="58.697, 19.6, 56.1, 4.13", headers={'Content-Type': 'text/csv'}).json()



*****************
Real applications
*****************
- For a UART to MQTT gateway implementation, see :ref:`beradio-python <beradio-python>`.
- For an example about how to run a unique realm on your own hardware, see:

  - https://github.com/Hiverize/Sensorbeuten/pull/1
  - https://github.com/hiveeyes/Hiverize-Sensorbeuten/blob/hiveeyes-backend/backend.rst
