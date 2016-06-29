.. include:: ../../_resources.rst

.. _forward-http-to-influx:

###########################
Forwarding HTTP to InfluxDB
###########################

*****
Intro
*****
For enabling :ref:`data-export` via HTTP, just forward GET requests to
InfluxDB and let the transformation machinery handle all the rest.

:ref:`data-export` means access to raw data in different
output formats as well as data plots.

*****
Setup
*****
This can be achieved by configuring a generic HTTP-to-InfluxDB
forwarder application:

.. literalinclude:: ../../_static/content/etc/examples/forwarders/http-to-influx.ini
    :language: ini
    :linenos:
    :emphasize-lines: 43-53

