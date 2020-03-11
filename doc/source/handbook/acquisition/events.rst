.. include:: ../../_resources.rst

.. _events-api:

##########
Events API
##########


.. _daq-mqtt-annotation:
.. _daq-mqtt-events:

MQTT events
===========
`Grafana Annotations`_ can be created through MQTT at the ``/event.json`` topic suffix.
While arbitrary fields can be submitted, Grafana_ evaluates the fields ``title``, ``text`` and ``tags``.
It is possible to use HTML inside the ``text`` field, for example to link this event to another web application.


The synopsis is::

    # Define channel.
    export MQTT_BROKER=localhost
    export MQTT_TOPIC=mqttkit-1/testdrive/area-42/node-1

    # Publish event.
    mosquitto_pub -h $MQTT_BROKER -t $MQTT_TOPIC/event.json -m '{"title": "Some event", "text": "<a href=\"https://somewhere.example.org/events?reference=482a38ce-791e-11e6-b152-7cd1c55000be\">see also</a>", "tags": "event,alert,important", "reference": "482a38ce-791e-11e6-b152-7cd1c55000be"}'

Annotations can also be submitted retroactively, just add a ``time`` field::

    mosquitto_pub -h $MQTT_BROKER -t $MQTT_TOPIC/event.json -m '{"time": "2016-12-07T17:30:15.842428Z", "title": "Some event in the past"}'

See also the whole list of :ref:`daq-timestamp-formats`.


.. _daq-http-annotation:
.. _daq-http-events:

HTTP events
===========
`Grafana Annotations`_ can be created through the HTTP interface at the ``/event`` endpoint.
While arbitrary fields can be submitted, Grafana_ evaluates the fields ``title``, ``text`` and ``tags``.
It is possible to use HTML inside the ``text`` field, for example to link this event to another web application.

The synopsis is::

    http POST http://localhost:24642/api/mqttkit-1/testdrive/area-42/node-1/event title='Some event' text='<a href="https://somewhere.example.org/events?reference=482a38ce-791e-11e6-b152-7cd1c55000be">see also</a>' tags='event,alert,important' reference='482a38ce-791e-11e6-b152-7cd1c55000be'

Annotations can also be submitted retroactively, just add a ``time`` field::

    http POST http://localhost:24642/api/mqttkit-1/testdrive/area-42/node-1/event time=2016-12-07T17:30:15.842428Z title='Some event in the past'

See also the whole list of :ref:`daq-timestamp-formats`.
