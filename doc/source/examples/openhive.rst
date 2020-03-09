.. include:: ../_resources.rst

.. _vendor-openhive:

#########
Open Hive
#########
There's some support for proprietary/legacy data formats on top of :ref:`daq-http`.
Here, the service understands a custom header format starting with "Datum/Zeit" or "Date/Time", like::

    echo 'Datum/Zeit,Gewicht,Aussen-Temperatur,Aussen-Feuchtigkeit,Spannung' | http POST http://localhost:24642/api/mqttkit-1/testdrive/area-42/node-1/data Content-Type:text/csv

Sensor readings are transmitted using local time.
On further processing, we assume them being in Central European Time (CET).
Example::

    echo '2016/08/14 21:02:06,  58.697, 19.6, 56.1, 4.13' | http POST http://localhost:24642/api/mqttkit-1/testdrive/area-42/node-1/data Content-Type:text/csv

.. tip::

    While this is possible, you should definitively favor using the established conventions, so please:

    - send timestamps using the field name ``time``
    - send timestamps in `ISO 8601`_ format, using UTC
