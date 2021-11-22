############################
Running Kotori with RabbitMQ
############################

Instead of Mosquitto, Kotori can be used together with `RabbitMQ`_ and its
`MQTT Plugin`_.

This is a basic description how to run RabbitMQ using Docker, in order to
verify the functionality.

::

    docker build --tag=rabbitmq-mqtt - < packaging/dockerfiles/rabbitmq.dockerfile

::

    docker run -it --rm --publish=1883:1883 --publish=15672:15672 rabbitmq-mqtt

Visit http://localhost:15672/ and log in with guest / guest.


.. _MQTT Plugin: https://www.rabbitmq.com/mqtt.html
.. _RabbitMQ: https://www.rabbitmq.com/
