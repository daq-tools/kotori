.. _kotori-troubleshooting:


***************
Troubleshooting
***************


No data in Grafana I
====================
- Q: I don't see any data!
- A: Most probably, your system time is wrong or deviates from the time of the system accessing Grafana from.
  For example, you won't see any data if the server time is in the future.

.. tip::

    So, either enable the NTP feature of ``systemd``::

        timedatectl set-ntp true

    or install ``chrony``::

        apt install chrony

    or implement any other valid equivalent to keep the system time sound.


No data in Grafana II
=====================
- Q: I still don't see any data!
- A: Try to increase the log level by adding ``--debug-foobar`` command line options to ``/etc/default/kotori``
  and get back to us, stacktrace or GTFO.
  See ``/opt/kotori/bin/kotori --help`` for available options.

Example ``/etc/default/kotori``::

    KOTORI_OPTS="--debug-mqtt --debug-influx"
