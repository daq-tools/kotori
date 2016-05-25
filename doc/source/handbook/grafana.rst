.. include:: ../_resources.rst

.. _grafana-handbook:

################
Grafana Handbook
################


*********************
Linking and embedding
*********************
It is pretty easy to link to and embed Grafana dashboards and panels.

For linking to whole dashboards, use the ``/dashboard`` entrypoint:

    https://swarm.hiveeyes.org/grafana/dashboard/db/hiveeyes-labs-wedding?from=now-24h&to=now

For linking to or embedding single panels without any chrome, use the ``/dashboard-solo``
entrypoint and select the designated panel using the query parameter ``panelId=5``:

    https://swarm.hiveeyes.org/grafana/dashboard-solo/db/hiveeyes-labs-wedding?panelId=5&from=now-24h&to=now

    .. raw:: html

        <iframe src="https://swarm.hiveeyes.org/grafana/dashboard-solo/db/hiveeyes-labs-wedding?panelId=5&from=now-24h&to=now" width="100%" height="425" frameborder="0"></iframe>


***********
Time ranges
***********

Specification
=============

- `Override dashboard time range with from and to URL parameters <https://github.com/grafana/grafana/issues/787>`_,
  4 different formats are supported as of 2014-09-10:

    - relative time::

        from=now-1h
        to=now

    - only date (utc) YYYYMMDD::

        from=20140301
        to=20140301

    - date and time (utc) YYYYMMDDTHHmmss::

        from=20140301T040210
        to=20140301T052010

    - epoch in ms (utc)::

        from=1410338479775
        to=1410338492279


- `Time Range Controls <http://docs.grafana.org/reference/timerange/>`_


Examples
========

relative time
-------------
Last 24 hours of data.

.. raw:: html

    <iframe src="https://swarm.hiveeyes.org/grafana/dashboard-solo/db/hiveeyes-labs-wedding?panelId=5&from=now-24h&to=now" width="100%" height="425" frameborder="0"></iframe>

.. container::

    https://swarm.hiveeyes.org/grafana/dashboard-solo/db/hiveeyes-labs-wedding?panelId=5&from=now-24h&to=now

|clearfix|

absolute time
-------------
Navigate to a specific time range with boundaries formatted as human readable datetime string.

.. raw:: html

    <iframe src="https://swarm.hiveeyes.org/grafana/dashboard-solo/db/hiveeyes-labs-wedding?panelId=5&from=20160519T040000&to=20160519T170000" width="100%" height="425" frameborder="0"></iframe>

.. container::

    https://swarm.hiveeyes.org/grafana/dashboard-solo/db/hiveeyes-labs-wedding?panelId=5&from=20160519T040000&to=20160519T170000

    This is a weight-loss event from :ref:`hiveeyes-scale-beutenkarl`
    recorded on 2016-05-20 between 10:11 and 10:26 hours CEST after a
    bee colony started swarming at the Hiveeyes Labs Beehive in Berlin Wedding,
    see also :ref:`hiveeyes-schwarmalarm-2016-05-20`.

|clearfix|

.. note::

    Please recognize the offset in absolute hours when viewing this from a different time zone than UTC.
    In european summer, we usually have CEST_, which has an UTC Offset of "UTC +2".

