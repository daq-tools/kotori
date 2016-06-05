.. include:: ../../_resources.rst

.. _protocol-forwarders:

###################
Protocol forwarders
###################
Protocol forwarder applications have an important
role inside the modular Kotori toolkit.

They can be used for making Kotori acquire data through POST/PUT requests to
defined HTTP endpoints and will be the foundation for generic udp acquisition,
for emitting telemetry data to the WAMP bus and finally for querying the
database through HTTP.

.. toctree::
    :maxdepth: 1
    :glob:

    http-to-mqtt

.. todo::

    - mqtt-to-wamp
    - udp-to-mqtt
    - influx-to-http (maybe via Grafana)

