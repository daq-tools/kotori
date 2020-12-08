.. _basic-mqtt-example:

#######################
Basic example with MQTT
#######################


Introduction
============
In this example, we will configure an example application with Kotori based
on the :ref:`application-mqttkit` communication style. We will use MQTT as
communication protocol and JSON as data serialization format.
After activating the configuration and submitting a telemetry packet,
a Grafana dashboard will be created automatically.

To read about all available options for MQTT data acquisition, please follow
up at :ref:`daq-mqtt`.


Configure Kotori application
============================
- ::

    cp /etc/kotori/examples/mqttkit.ini /etc/kotori/apps-available/amazonas.ini

- Edit::

    realm       = amazonas
    mqtt_topics = amazonas/#

- Activate::

    ln -s /etc/kotori/apps-available/amazonas.ini /etc/kotori/apps-enabled/

- Watch Kotori logfile::

    tail -F /var/log/kotori/kotori.log

- Restart Kotori::

    systemctl restart kotori


Send sample telemetry packet
============================
::

    aptitude install mosquitto-clients

::

    CHANNEL_TOPIC=amazonas/ecuador/cuyabeno/1/data.json
    mosquitto_pub -t $CHANNEL_TOPIC -m '{"temperature": 42.84, "humidity": 83.1}'


Watch telemetry data
====================
- Access Grafana by navigating to http://kotori.example.org:3000/ and logging in with ``admin/admin``.
- Navigate to the dashboard just created by submitting telemetry data
  http://kotori.example.org:3000/dashboard/db/amazonas-ecuador.


Troubleshooting
===============
If you experience problems or don't see any data in Grafana,
please follow up with :ref:`kotori-troubleshooting`.
