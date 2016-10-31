.. include:: ../../../_resources.rst

.. _daq-python:

############################
Data acquisition with Python
############################
.. highlight:: python


****
MQTT
****
- `paho-mqtt`_, the MQTT Python client library from the `Eclipse Paho`_ project
- .. todo::

    Add complete MQTT example with Python. In the meanwhile, see :ref:`beradio-python <beradio-python>` and

    - https://github.com/Hiverize/Sensorbeuten/pull/1
    - https://github.com/hiveeyes/Hiverize-Sensorbeuten/blob/hiveeyes-backend/backend.rst


****
HTTP
****

Requests
========
.. highlight:: bash

Setup
-----
Choose one of these for installing Requests_::

    # Debian
    aptitude install python-requests

    # Macports
    port install py-requests

    # Vanilla Python
    pip install requests


.. _daq-python-http:

.. _daq-python-requests:

Transmit
--------
.. highlight:: python

::

    import requests
    data = {"temperature": 42.84, "humidity": 83}

    # Post as application/json
    requests.post("http://localhost:24642/api/bus/mqtt/mqttkit-1/testdrive/area-42/node-1/data", json=data).content

    # Post as application/x-www-form-urlencoded
    requests.post("http://localhost:24642/api/bus/mqtt/mqttkit-1/testdrive/area-42/node-1/data", data=data).content


HTTPie
======

Setup
-----
.. highlight:: bash

Choose one of these for installing HTTPie_::

    # Debian
    aptitude install httpie

    # Macports
    port install httpie

    # Vanilla Python
    pip install httpie


.. _daq-httpie:

.. _daq-python-httpie:

Transmit
--------
.. highlight:: bash

::

    # Post as application/json
    http POST http://localhost:24642/api/bus/mqtt/mqttkit-1/testdrive/area-42/node-1/data temperature:=42.84 humidity:=83

    # Post as application/x-www-form-urlencoded
    http --form POST http://localhost:24642/api/bus/mqtt/mqttkit-1/testdrive/area-42/node-1/data temperature:=42.84 humidity:=83

***
UDP
***
.. seealso:: :ref:`daq-udp`

