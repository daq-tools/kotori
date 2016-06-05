.. include:: ../../../_resources.rst

.. _daq-http:

##########################
Data acquisition over HTTP
##########################

.. tip::

    For making Kotori listen to HTTP requests for telemetry data acquisition,
    please have a look at :ref:`forward-http-to-mqtt` about how to configure
    a HTTP endpoint for your :ref:`application-mqttkit` application.

************
HTTP clients
************

.. list-table:: List of Kotori HTTP clients
   :widths: 10 40
   :header-rows: 1
   :class: table-generous

   * - Name
     - Description

   * - curl
     - See :ref:`daq-curl` for an example how to transmit telemetry data using curl.

   * - HTTPie
     - See :ref:`transmit using HTTPie <daq-httpie>` when preferring HTTPie_, a cURL-like tool for humans.

   * - Python
     - See :ref:`transmit from Python <daq-python-http>` using the fine Requests_ http library.

   * - PHP
     - Visit :ref:`daq-php` for a library and and an example how to transmit telemetry data from PHP.

