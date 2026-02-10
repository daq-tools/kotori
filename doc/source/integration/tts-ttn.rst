.. include:: ../_resources.rst

.. _tts-ttn-decoder:
.. _integration-tts-ttn:

#####################################
The Things Stack & Network (TTS, TTN)
#####################################


*****
About
*****

Receive and decode telemetry data from devices on the `LoRaWAN`_ network controller
implementation `The Things Stack (TTS)`_ / `The Things Network (TTN)`_, using HTTP
`webhooks`_, and store it into timeseries databases for near real-time querying.

.. figure:: https://upload.wikimedia.org/wikipedia/commons/b/bb/The_Things_Network_logo.svg
    :target: https://de.wikipedia.org/wiki/The_Things_Network
    :alt: The Things Network logo
    :width: 100px

Overview
========

.. Mermaid Flowcharts documentation: https://mermaid.js.org/syntax/flowchart.html

.. mermaid::

    %%{init: {"flowchart": {"defaultRenderer": "dagre", "htmlLabels": false}} }%%

    flowchart LR

      subgraph sensors [sensor domain]
        direction LR
        Device
      end

      subgraph network [The Things Network]
        direction TB
        TTS[The Things Stack\nLoRaWAN Network Server]
        TTS -.-> Webhook[HTTP Webhook]
      end

      subgraph backend
        direction LR
        Kotori --> InfluxDB
        Kotori --> Grafana
      end

      sensors -.- RF/ISM/LoRaWAN -.-> network
      network ==> backend

Background
==========

The TTS documentation states that their long-term data storage feature is not suitable
for real-time querying.

    The `TTS Storage Integration`_ should not be used for querying realtime data. For
    scalability reasons, writes to the Storage Integration database are performed in batches
    and there may be a delay after an uplink is received, before it is available. For realtime
    alerts, use Webhooks.

Glossary
========

:The Things Stack (TTS): A robust, yet flexible `LoRaWAN`_ Network Server for demanding
    LoRaWAN deployments, from covering the essentials to advanced security configurations
    and device life cycle management.

:The Things Network (TTN): An open community-based initiative to build a low-power,
    wide-area network for the Internet of Things.

:TTS Webhooks: Allows *The Things Stack* to send application related messages to specific
    HTTP(S) endpoints.


*****
Setup
*****

Getting the system configured properly is important, please read this section carefully.

Creating a custom webhook
=========================

You will need to use `The Things Network Console`_ at
https://console.cloud.thethings.network/, in order to `configure a custom Webhook`_.

On the custom webhook configuration dialog, please enter the following settings:

- **Webhook ID**

  An arbitrary label identifying the Webhook.

- **Webhook format**

  Choose ``JSON`` here.

- **Base URL**

  Like outlined at the :ref:`daq-http` documentation section, this setting will obtain
  the full URL to the data acquisition channel, modulo the ``/data`` suffix, which will
  be added per "Enabled event types" configuration option.

- **Filter event data**

  If you want to filter the submitted telemetry payload, and only submit the nested
  ``decoded_payload`` data structure, you can use a path accessor expression like
  ``up.uplink_message.decoded_payload``. Check out all available `filter paths`_.

- **Enabled event types**

  For the event type ``Uplink message``, add the URL path suffix ``/data``.

This screenshot of the corresponding dialog in TTS guides you which parameters to
configure correspondingly.

.. figure:: https://github.com/daq-tools/kotori/assets/453543/c808412a-7ce1-4733-84a4-c4adab67985f
    :target: https://github.com/daq-tools/kotori/assets/453543/c808412a-7ce1-4733-84a4-c4adab67985f
    :alt: The Things Network Console Webhook configuration
    :width: 600px

    *The Things Network Console Webhook configuration*

.. important::

    If you want to receive the full TTN message payload, in order to decode additional
    metadata, for example gateway information, please leave the ``Filter event data``
    field empty.

Now, when the TTN infrastructure receives uplink messages from your device(s), they will
be delivered to the configured HTTP endpoint in JSON format. Kotori will decode those
messages transparently.

Single-device connectivity
==========================

If you only want to connect a few devices, and want to configure individual webhooks for
them, you may find it acceptable to create a dedicated `TTS Application`_ **per device**.

A corresponding set of example default values, when using the "wide" channel addressing
scheme, in order to dispatch messages to channels of individual devices, would be::

    Webhook ID:             expert-bassoon
    Webhook format:         JSON
    Base URL:               https://daq.example.org/api/sensorwan-1/testdrive/area42/node1
    Filter event data:      up.uplink_message.decoded_payload
    Enabled event types:    /data

.. note::

    With this configuration variant, you will configure the full-qualified SensorWAN
    address within the "Base URL" field of your application.

.. _ttn-multi-tenant:

Multi-tenant connectivity
=========================

The `multi-tenant`_ connectivity option allows you to use a **single** `TTS Application`_
to serve multiple :ref:`hiveeyes-arduino:sensorwan` networks, in order to support a fleet
of devices, without needing to create individual, per-device webhooks.

This is a corresponding set of example default values, when using the "direct" channel
addressing scheme, in order to multiplex channels of different devices using a single
HTTP endpoint, effectively implementing `trunking`_ data acquisition::

    Webhook ID:             fuzzy-carnival
    Webhook format:         JSON
    Base URL:               https://daq.example.org/api/sensorwan-1/channel{/devID}
    Filter event data:
    Enabled event types:    /data

.. note::

    This example uses a single webhook configuration based on using the ``{/devID}`` path
    variable within the "Base URL" field of your application. You can learn about other path
    variables at `TTS Webhook Path Variables`_.

    It also leaves the "Filter event data" field empty, so you will receive full payloads,
    including metrics from gateways, etc.


****************
Dry-run examples
****************

By using the following examples, you can exercise the transmission procedure within
a dry-run environment / sandbox.

.. literalinclude:: tts-ttn-uplink.json
    :language: json

Acquire and submit a minimal TTN JSON payload to Kotori's HTTP API.

.. code-block:: shell

    wget https://github.com/daq-tools/kotori/raw/main/test/test_tts_ttn_minimal.json
    cat test_tts_ttn_minimal.json | \
        http POST https://daq.example.org/api/sensorwan-1/testdrive/area42/node1/data

Acquire and submit a full TTN JSON payload to Kotori's HTTP API.

.. code-block:: shell

    wget https://github.com/daq-tools/kotori/raw/main/test/test_tts_ttn_full.json
    cat test_tts_ttn_full.json | \
        http POST https://daq.example.org/api/sensorwan-1/testdrive/area42/node1/data

.. note::

    | Addressing the same channel using the "direct" variant means replacing
    | ``/testdrive/area42/node1`` by
    | ``/channel/testdrive-area42-node1``.

    A full-qualified URL example is::

        https://daq.example.org/api/sensorwan-1/channel/testdrive-area42-node1/data

.. tip::

    For submitting JSON data to the HTTP endpoint of Kotori, the examples above are using
    the excellent `HTTPie`_ program. Note that the same requests can also be submitted
    by using the `curl`_ program, or any other HTTP client.


******************
Grafana screenshot
******************

This is an example screenshot of a `Grafana`_ dashboard, which demonstrates the outcome
of LoRaWAN transmissions.

.. figure:: https://github.com/daq-tools/kotori/assets/453543/45786928-d54a-4052-a124-f4adac3b5604
    :target: https://swarm.hiveeyes.org/grafana/d/763KRx7mk/freiland-potsdam-thias-lora-multi-hive
    :alt: LoRaWAN/TTN Grafana example dashboard


.. _configure a custom Webhook: https://www.thethingsindustries.com/docs/integrations/webhooks/
.. _filter paths: https://www.thethingsindustries.com/docs/integrations/webhooks/webhook-templates/format/#field-mask
.. _HTTPie: https://httpie.io/
.. _The Things Stack (TTS): https://www.thethingsindustries.com/docs/
.. _The Things Network (TTN): https://www.thethingsnetwork.org/
.. _The Things Network Console: https://www.thethingsnetwork.org/docs/network/console/
.. _The Things Network Console - Creating Webhooks: https://www.thethingsindustries.com/docs/integrations/webhooks/creating-webhooks/
.. _TTS Application: https://www.thethingsindustries.com/docs/integrations/adding-applications/
.. _TTS Webhook Path Variables: https://www.thethingsindustries.com/docs/integrations/webhooks/path-variables/
.. _TTS Storage Integration: https://www.thethingsindustries.com/docs/integrations/storage/
