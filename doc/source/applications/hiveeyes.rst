.. include:: ../_resources.rst

.. _vendor-hiveeyes:

########
Hiveeyes
########

.. contents::
   :local:
   :depth: 1

----

*****
About
*****
Together with Mosquitto_, InfluxDB_, Grafana_, mqttwarn_ and BERadio_,
Kotori runs the data collection hub ``swarm.hiveeyes.org`` (the `Hiveeyes platform`_)
for a Berlin-based beekeeper collective.

For source code, have a look at `Hiveeyes at GitHub`_.

Feel welcome to join us: hiveeyes-devs ät ideensyndikat.org


*******
Details
*******

URL entrypoints
===============
Entrypoints to the platform running on ``swarm.hiveeyes.org`` as of 2016-01-29:

- | Mosquitto
  | mqtt://swarm.hiveeyes.org
- | Grafana
  | https://swarm.hiveeyes.org/grafana/


Serial to MQTT forwarding
=========================
This has completely moved to the scope of BERadio_. Nothing to see here. :-)



*******************
Platform operations
*******************

Install the platform
====================
The most convenient way is by using Debian packages for all
infrastructure services and Kotori, see :ref:`setup-debian`.
After that, the service should have been automatically started
by systemd so the system is ready to serve requests.

InfluxDB
========
For working directly with the InfluxDB_ API, please have a look at the :ref:`influxdb-handbook`.




********************
Platform development
********************

Want to see more? Read on my dear.

Setup
=====
When developing on Kotori or for ad-hoc installations, you should follow the
"instructions for installing Kotori as :ref:`setup-python-package`".

Run Kotori
==========
In ad-hoc installations, or when turning off the systemd service,
you might want to start Kotori interactively in the foreground::

    /opt/kotori/bin/kotori --config /etc/kotori/kotori.ini --debug

Hacking
=======
For getting your development sandbox up and running,
please have a look at :ref:`kotori-hacking`.

.. note::
    Please contact us by email at "hiveeyes-devs ät ideensyndikat.org"
    for repository access until the source code is on GitHub.


********
Wishlist
********
- Aggregate measurements over time ranges (e.g. daily) and republish summary to MQTT

    - Provide reasonable "delta" values in relation to the point of last summary
    - Proposal for summary topics: hiveeyes/username/summary/foo/daily/bar
    - Schedule at: Morning, Noon, Evening

- Threshold alerting
- `Weather data publishing <../development/weather.html>`_
- "Stockkarte" subsystem

    - marking point in graphs and filling the Stockkarte questioning
    - https://github.com/Dieterbe/anthracite/
    - https://twitter.github.io/labella.js/

- Timeseries anomaly detection using machine learning


**************
Under the hood
**************

The most desirable thing to amend when hacking on Kotori in the context of Hiveeyes might be the routing
code of how to map inbound MQTT data messages appropriately into InfluxDB databases and time series (tables).

When using the »quadruple hierarchy strategy«, a data message sent to the MQTT topic ``hiveeyes/999/1/99``
will be stored in a database named ``hiveeyes_999`` and a series named ``1_99``::

    hiveeyes  /  999  /  1  /  99
    |                 |         |
    |    database     | series  |
    |  hiveeyes_999   |  1_99   |
    |                 |         |

Find the routines implementing this strategy in ``kotori/vendor/hiveeyes/application.py``, lines 44 ff.:
