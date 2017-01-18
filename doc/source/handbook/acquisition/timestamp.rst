.. include:: ../../_resources.rst

.. _daq-timestamp-formats:

*****************
Timestamp formats
*****************
Timestamped readings can be submitted in different formats using the data field ``time``.

.. list-table:: Supported timestamp formats
    :widths: 30 50
    :header-rows: 1
    :class: table-generous

    * - Example
      - Description

    * - 2016-12-07T17:30:15.842428Z
      - Human readable timestamp in `ISO 8601`_ format, UTC

    * - 2016-12-07T18:30:15+0100
      - Human readable timestamp, also `ISO 8601`_, with UTC offset

    * - 2016-12-07T18:30:15 CET
      - `ISO 8601`_ with custom timezone offset: Central European Time (CET).

    * - 2016-12-07T18:30:15
      - `ISO 8601`_ without timezone.
        Assume Europe/Berlin (CET) if no timezone is given.
        It will also account for daylight saving time (DST),
        so there's no specific need to use CEST vs. CET during summer.

    * - | 1481131815000000000
        | 1481131815000000
        | 1481131815000
        | 1481131815
      - `Unix time`_ in nano-, micro- milli-, or whole seconds.

.. note::

    - Use http://www.epochconverter.com/ for converting epoch to human readable date and vice versa.
    - Have a look at http://www.epochconverter.com/#code for doing the same programmatically.

