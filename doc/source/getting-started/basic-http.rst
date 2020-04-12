.. _basic-http-example:

#######################
Basic example with HTTP
#######################


Introduction
============
In this example, we will configure an example application with Kotori based
on the :ref:`application-mqttkit` communication style. We will use HTTP as
communication protocol and JSON as data serialization format. It builds upon
the :ref:`basic-mqtt-example`.

To read about all available options for HTTP data acquisition, please follow
up at :ref:`daq-http`.


Configure Kotori application
============================
- Add this snippet to ``/etc/kotori/apps-enabled/amazonas.ini`` and edit::

    realm       = amazonas
    source      = http:/api/amazonas/...
    target      = mqtt:/amazonas/...

.. highlight:: ini

Take a look at :download:`etc/examples/forwarders/http-api-generic.ini <../_static/content/etc/examples/forwarders/http-api-generic.ini>`
as a configuration blueprint.

.. literalinclude:: ../_static/content/etc/examples/forwarders/http-api-generic.ini
    :language: ini
    :linenos:
    :lines: 1-42
    :emphasize-lines: 34-42

- Watch Kotori logfile::

    tail -F /var/log/kotori/kotori.log

- Restart Kotori::

    systemctl restart kotori


Send sample telemetry packet
============================
::

    CHANNEL_URI=http://localhost:24642/api/amazonas/ecuador/cuyabeno/1/data
    echo '{"temperature": 42.84, "humidity": 83.1}' | curl --request POST --header 'Content-Type: application/json' --data @- $CHANNEL_URI


Watch telemetry data
====================
- Access Grafana by navigating to http://kotori.example.org:3000/ and logging in with ``admin/admin``.
- Navigate to the dashboard just created by submitting telemetry data
  http://kotori.example.org:3000/dashboard/db/ecuador.


Troubleshooting
===============
If you experience problems or don't see any data in Grafana,
please follow up with :ref:`kotori-troubleshooting`.
