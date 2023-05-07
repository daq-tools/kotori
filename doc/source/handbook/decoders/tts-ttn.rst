.. include:: ../../_resources.rst

.. _tts-ttn-decoder:

###############
TTS/TTN decoder
###############


*****
About
*****

Receive and decode telemetry data from devices on the `The Things Stack (TTS)`_
/ `The Things Network (TTN)`_.

.. figure:: https://upload.wikimedia.org/wikipedia/commons/b/bb/The_Things_Network_logo.svg
    :target: https://de.wikipedia.org/wiki/The_Things_Network
    :alt: The Things Network logo
    :width: 100px


*************
Configuration
*************

Getting the system configured properly is important, please read this section carefully.


The Things Network Console
==========================

First, you will need to use `The Things Network Console`_ at
https://console.cloud.thethings.network/, in order to `configure an outbound Webhook`_.

.. figure:: https://user-images.githubusercontent.com/453543/236702766-850c9bb3-06e8-4372-8192-0cb521d598a0.png
    :target: https://user-images.githubusercontent.com/453543/236702766-850c9bb3-06e8-4372-8192-0cb521d598a0.png
    :alt: The Things Network Console Webhook configuration
    :width: 640px

    *The Things Network Console Webhook configuration*

Please configure the following settings:

- ``Webhook ID``: An arbitrary label identifying the Webhook.
- ``Webhook format``: Choose ``JSON`` here.
- ``Base URL``: Like outlined at the :ref:`daq-http` documentation section, this
  setting will obtain the full URL to the data acquisition channel, modulo the
  ``/data`` suffix, which will be added per "Enabled event types" configuration
  option.
- ``Filter event data``: If you want to filter the submitted telemetry payload,
  and only submit the nested ``decoded_payload`` data structure, you can use a
  path accessor expression like ``up.uplink_message.decoded_payload``.
- ``Enabled event types``: For the event type ``Uplink message``, add the URL
  path suffix ``/data``.

Example
-------

This would be a corresponding set of example default values::

    Webhook ID:             expert-bassoon
    Webhook format:         JSON
    Base URL:               https://daq.example.org/api/mqttkit-1/testdrive/area-42/node-1
    Filter event data:      up.uplink_message.decoded_payload
    Enabled event types:    /data


*******
Example
*******

Now, JSON data payloads submitted from the TTN infrastructure to your system, like this
example, will be decoded by Kotori transparently.

.. literalinclude:: tts-ttn-uplink.json
    :language: json

.. todo::

    Provide an example how a corresponding message can be submitted to TTN
    from the terminal, in order to emulate the real scenario, but demonstrate
    the telemetry data acquisition works well, almost end-to-end. In the meanwhile,
    submit an example JSON message payload to Kotori's HTTP API directly::

        http https://github.com/daq-tools/kotori/raw/main/doc/source/handbook/decoders/tts-ttn-uplink.json \
            | http POST https://daq.example.org/api/mqttkit-1/testdrive/area-42/node-1/data


.. _configure an outbound Webhook: https://www.thethingsindustries.com/docs/integrations/webhooks/
.. _The Things Stack (TTS): https://www.thethingsindustries.com/docs/
.. _The Things Network (TTN): https://www.thethingsnetwork.org/
.. _The Things Network Console: https://www.thethingsnetwork.org/docs/network/console/
