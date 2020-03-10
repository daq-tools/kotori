.. include:: ../../_resources.rst

.. _grafana-handbook:

#######
Grafana
#######

.. admonition:: Please note

    This page is just a stub.


*********************
Linking and embedding
*********************
It is pretty easy to link to and embed Grafana dashboards and panels.

For linking to whole dashboards, use the ``/dashboard`` entrypoint:

    https://swarm.hiveeyes.org/grafana/dashboard/db/hiveeyes-labs-wedding?from=now-24h&to=now

For linking to or embedding single panels without any chrome, use the ``/dashboard-solo``
entrypoint and select the designated panel using the query parameter ``panelId=17``:

    https://weather.hiveeyes.org/grafana/d-solo/YVm0P1miz/meteogramm-einer-station-cdc-and-mosmix?orgId=1&fullscreen&panelId=17

    .. raw:: html

        <iframe src="https://weather.hiveeyes.org/grafana/d-solo/YVm0P1miz/meteogramm-einer-station-cdc-and-mosmix?orgId=1&fullscreen&panelId=17" width="100%" height="425" frameborder="0"></iframe>


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

    <iframe src="https://weather.hiveeyes.org/grafana/dashboard-solo/YVm0P1miz/meteogramm-einer-station-cdc-and-mosmix?fullscreen&panelId=17&from=now-24h&to=now" width="100%" height="425" frameborder="0"></iframe>

.. container::

    https://weather.hiveeyes.org/grafana/d/YVm0P1miz/meteogramm-einer-station-cdc-and-mosmix?fullscreen&panelId=17&from=now-24h&to=now

|clearfix|

absolute time
-------------
Navigate to a specific time range with boundaries formatted as human readable datetime string.

.. raw:: html

    <iframe src="https://swarm.hiveeyes.org/grafana/dashboard-solo/db/hiveeyes-labs-wedding?panelId=5&from=20160519T040000&to=20160519T170000" width="100%" height="425" frameborder="0"></iframe>

.. container::

    https://swarm.hiveeyes.org/grafana/dashboard-solo/db/hiveeyes-labs-wedding?panelId=5&from=20160519T040000&to=20160519T170000

    This is a weight-loss event from a :ref:`hive scale <hiveeyes-scale-beutenkarl>`
    recorded on 2016-05-20 between 10:11 and 10:26 hours CEST after a
    bee colony started swarming at the Hiveeyes Labs Beehive in Berlin Wedding,
    see also :ref:`hiveeyes-schwarmalarm-2016-05-20`.

|clearfix|
