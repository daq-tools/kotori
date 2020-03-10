.. include:: ../_resources.rst

.. _daq-php:

###
PHP
###

.. highlight:: php


*******
Library
*******
There is a convenient PHP library for interacting with Kotori over HTTP ready for download, see
:download:`terkin-http.php <../_static/content/clients/runtime/php/terkin-http.php>`.
If you're stuck with PHP4, see
:download:`terkin-http.php4 <../_static/content/clients/runtime/php/terkin-http.php4>`
for a version based on the PHP CURL binding and without namespaces.


Node API (highlevel)
====================
Transmitting telemetry data using PHP is pretty easy, read on my dear:

.. literalinclude:: ../_static/content/clients/runtime/php/terkin-http.php
    :language: php
    :lines: 18-37
    :linenos:
    :emphasize-lines: 18-20


Client API (lowlevel)
=====================
For transmitting telemetry data to an absolute uri, use the "Basic API" telemetry client object:

.. literalinclude:: ../_static/content/clients/runtime/php/terkin-http.php
    :language: php
    :lines: 43-45
    :linenos:



****
Demo
****

Command line
============
There is a command line program :download:`terkin-demo.php <../_static/content/clients/runtime/php/terkin-demo.php>`
for demonstration purposes, it will send data to ``localhost:24642``::

    php -f clients/runtime/php/terkin-demo.php run demo
    php -f clients/runtime/php/terkin-demo.php run sawtooth

.. note::

    ``24642`` is the default http port of Kotori. For making this work, Kotori
    should be configured similar to the canonical example configuration described
    in :ref:`application-mqttkit` and :ref:`forward-http-to-mqtt`.

The demo program in detail
==========================

.. literalinclude:: ../_static/content/clients/runtime/php/terkin-demo.php
    :language: php
    :linenos:
    :emphasize-lines: 27-31,37-45,55-57,61-66
