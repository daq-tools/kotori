.. include:: ../_resources.rst


############################################
Ingesting weather data from WeeWX using MQTT
############################################


************
Introduction
************
I'm writing a thesis about automatic acquisition of meteorological
data from the Davis Vantage Pro2 station and i'm using Kotori_ and WeeWX_ for that,
based on `Kotori's WeeWX integration <https://getkotori.org/docs/examples/weewx.html>`_.
I have a question about how Kotori_ ingests data to InfluxDB_.
Is it through HTTP GET requests? What does Kotori do to the JSON that comes from MQTT?

- Firstly, I utilized the `MQTT Plugin for WeeWX`_ to publish data to the MQTT broker with a specific topic.
- Then, I subscribed Kotori_ to that topic by specifying it in the configuration file ``weewx.ini``.
- By subscribing to that topic, I now have the JSON payload and now I want to ingest that data into
  InfluxDB_ accordingly. I don't want to publish again data into the broker like outlined within
  `MQTT data acquisition <https://getkotori.org/docs/handbook/acquisition/protocol/mqtt.html>`_.

----

**********************
Data ingest using MQTT
**********************

Question
========
Are you sure the data is ingested into InfluxDB through MQTT without using HTTP POST requests?

Answer
======
You are on the right path, that is exactly how it works. By publishing measurement data to the
MQTT_ bus and configuring Kotori_ appropriately, it will converge the data into the InfluxDB_
timeseries database without further ado.
Using HTTP POST is a different path for ingesting data, we will just use MQTT here.

----

*************************
Application configuration
*************************

.. highlight:: ini

Question
========
What does this ``application`` option in the configuration snippet mean?

::

    ; -----------------------------
    ; Data acquisition through MQTT
    ; -----------------------------
    [weewx]
    enable      = true
    type        = application
    realm       = weewx
    mqtt_topics = weewx/#
    application = kotori.daq.application.mqttkit:mqttkit_application


Answer
======
The core of each data acquisition application is its configuration object.
``application`` designates the machinery should invoke the entrypoint function
``mqttkit_application`` within the Python module ``kotori.daq.application.mqttkit``
for spawing an application.

For further details, see also
`mqttkit_application <https://github.com/daq-tools/kotori/blob/0.24.5/kotori/daq/application/mqttkit.py#L38-L40>`_
and the documentation section about the :ref:`application-object`.


----

.. _weewx-export:

**************
Exporting data
**************

.. highlight:: ini

Question
========
I have a question about the export of data from InfluxDB_ in the ``weewx.ini``
configuration file. My question is about the ``source``, ``target`` and
``transform`` options within the configuration snippet referenced below.

- The ``source`` option defines a HTTP GET request to the database.
- The ``target`` option is used to define the InfluxDB_ database and
  measurement where the timeseries data is stored.
- Maybe you can shed some more light onto the ``transform`` option.
- Is this snippet used to get the JSON payload published in order to put it into InfluxDB?
- Why is the export necessary if I can see data in Grafana already?

::

    ; ----------------------------------------------------------------------
    ; Data export
    ; https://getkotori.org/docs/handbook/export/
    ; https://getkotori.org/docs/applications/forwarders/http-to-influx.html
    ; ----------------------------------------------------------------------
    [weewx.data-export]
    enable          = true

    type            = application
    application     = kotori.io.protocol.forwarder:boot

    realm           = weewx
    source          = http:/api/{realm:weewx}/{network:.*}/{gateway:.*}/{node:.*}/{slot:(data|event)}.{suffix} [GET]
    target          = influxdb:/{database}?measurement={measurement}
    transform       = kotori.daq.intercom.strategies:WanBusStrategy.topology_to_storage,
                      kotori.io.protocol.influx:QueryTransformer.transform


Answer
======
    Is this snippet used to get the JSON payload published in order to put it into InfluxDB?

It is rather about "retreiving" the data from InfluxDB. This snippet implements the **data export functionality**.

    Maybe you can shed some more light onto the ``transform`` option.

This is how you read this configuration snippet:

    The ``source`` option defines a HTTP GET endpoint which, when requested,
    will run an InfluxDB query against the thing defined by ``target`` after being
    transformed through the machinery defined by ``transform``.

All the heavy lifting is under the hood and implemented by the designated
software components like WanBusStrategy_ and QueryTransformer. The
configuration object just ties things together.

The ``transform`` setting is for defining components which take the request
data and build a sensible InfluxDB query and appropriate request from it in
order to pull data from InfluxDB.


**********
Conclusion
**********
We hope this will shed more light onto the whole thing how data is flowing
from WeeWX_ over MQTT_ through the Kotori_ into InfluxDB_ and how it is
finally displayed within Grafana_.

All of these mechanisms and subsystems have been designed to a) get you
started with data acquisition and graphing instantly and b) will give
you the freedom to establish any number of data acquisition channels
without having to provision them explicitly beforehand.
The motto here is: Just throw a bunch of JSON at the system.

Feel free to ask for more specific things which might still be unclear.


*********
Resources
*********
- https://community.hiveeyes.org/t/messdaten-an-die-hiveeyes-plattform-ubermitteln/1813
- https://community.hiveeyes.org/t/how-do-measurements-flow-from-mqtt-to-grafana/729
- https://github.com/daq-tools/kotori/issues/12
- https://github.com/daq-tools/kotori/issues/13
