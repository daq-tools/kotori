.. include:: ../../_resources.rst

.. _protocol-forwarders:

###################
Protocol forwarders
###################
Protocol forwarder applications have an important
role inside the modular Kotori toolkit.

They can be used for data acquisition through POST/PUT requests to
defined HTTP endpoints, data querying and export through GET requests
and will be the foundation for generic udp acquisition and for emitting
telemetry data to the WAMP bus.

.. toctree::
    :maxdepth: 1
    :glob:

    http-to-mqtt
    http-to-influx

.. todo::

    - mqtt-to-wamp
    - udp-to-mqtt

