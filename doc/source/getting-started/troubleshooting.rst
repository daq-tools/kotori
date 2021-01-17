.. _kotori-troubleshooting:


***************
Troubleshooting
***************


Introduction
============
Kotori's log output is directed to ``/var/log/kotori/kotori.log``. If you
experience any troubles, the first idea should be to review it.


No data in Grafana I
====================
- Q: I don't see any data!
- A: Most probably, Kotori does not have appropriate access to the Grafana instance.
  This might happen on the initial installation after Grafana encouraged you to change
  the default credentials away from admin/admin. If you did so, please adjust Kotori's
  configuration within e.g. ``/etc/kotori/kotori.ini``.


No data in Grafana II
=====================
- Q: I still don't see any data!
- A: Most probably, your system time is wrong or deviates from the time of the system accessing Grafana from.
  For example, you won't see any data if the server time is in the future.

.. tip::

    So, either enable the NTP feature of ``systemd``::

        timedatectl set-ntp true

    or install ``chrony``::

        apt install chrony

    or implement any other valid equivalent to keep the system time sound.


No data in Grafana III
======================
- Q: I still don't see any data!
- A: Try to increase the log level by adding ``--debug-foobar`` command line options to ``/etc/default/kotori``
  and get back to us, stacktrace or GTFO.
  See ``/opt/kotori/bin/kotori --help`` for available options.

Example ``/etc/default/kotori``::

    KOTORI_OPTS="--debug-mqtt --debug-influx"
