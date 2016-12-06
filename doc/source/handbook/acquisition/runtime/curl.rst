.. include:: ../../../_resources.rst

.. _daq-curl:

##########################
Data acquisition with curl
##########################
.. highlight:: bash

::

    # Define HTTP endpoint
    export HTTP_HOST="localhost:24642"

    # Define MQTT target topic
    export DEVICE_REALM="mqttkit-1"
    export DEVICE_TOPIC="testdrive/area-42/node-1"

    # Send JSON data
    echo '{"temperature": 42.84, "humidity": 83}' | curl --request POST --header 'Content-Type: application/json' --data @- http://$HTTP_HOST/api/$DEVICE_REALM/$DEVICE_TOPIC/data

    # Send urlencoded data
    echo 'temperature=42.84&humidity=83' | curl --request POST --header 'Content-Type: application/x-www-form-urlencoded' --data @- http://$HTTP_HOST/api/$DEVICE_REALM/$DEVICE_TOPIC/data


.. seealso:: :ref:`Transmit a periodic sawtooth signal over HTTP <sawtooth-http>`

