.. include:: ../../_resources.rst

.. _http-api-export:

#############################
HTTP export API configuration
#############################

************
Introduction
************
For enabling :ref:`data-export` via HTTP, just forward GET requests to the timeseries
database, and let the transformation machinery handle all the rest.

:ref:`data-export` means access to raw data in different
output formats as well as data plots.

*****
Setup
*****
This can be achieved by configuring a generic forwarder application:

.. literalinclude:: ../../_static/content/etc/examples/forwarders/http-api-export.ini
    :language: ini
    :linenos:
    :emphasize-lines: 43-53

