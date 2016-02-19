.. include:: ../_resources.rst

.. _vendor-hiveeyes:

########
Hiveeyes
########

.. contents::
   :local:
   :depth: 2

----

*****
Intro
*****

Together with Mosquitto_, InfluxDB_, Grafana_ and BERadio_, Kotori runs
the data collection hub ``swarm.hiveeyes.org`` (the `Hiveeyes platform`_)
for a Berlin-based beekeeper collective.

Feel welcome to join us: hiveeyes-devs ät ideensyndikat.org


*******************
Platform operations
*******************

Install the platform
====================
The most convenient way is by using Debian packages for all
infrastructure services and Kotori, see :ref:`setup-debian`.


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


InfluxDB
========
For working directly with the InfluxDB_ API, please have a look at the :ref:`influxdb-handbook`.



********************
Platform development
********************

Want to see more? Read on my dear.

Under the hood
==============
Kotori can be installed in different variants.

    - Install Python source Egg with ``pip``::

        # prepare system
        aptitude install python-pip build-essential python-dev libffi-dev libssl-dev

        # install latest Kotori release with feature "daq"
        pip install kotori[daq] --extra-index-url=https://packages.elmyra.de/hiveeyes/python/eggs/ --upgrade

.. tip::

    Installing Kotori with ``pip`` inside a Python *virtualenv* would
    be perfect when playing around. You won't need root permissions
    and the Python libraries of your system distribution will stay
    completely untouched.
    See also :ref:`kotori-hacking` for more information about that.


The Egg
-------
| Q: What is this? Give me the Egg!
| A: Here you are:

    https://packages.elmyra.de/hiveeyes/python/eggs/kotori/kotori-0.6.0.tar.gz


Run Kotori
==========
Usually, the service should have been automatically started by systemd.
However, when turning this off, you might want to play around interactively::

    /opt/kotori/bin/kotori --config /etc/kotori/kotori.ini --debug


Hacking
=======
For getting your development sandbox up and running, you might want to read :ref:`kotori-hacking` first.

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

.. highlight:: python

::

    class HiveeyesApplication(object):

        # [...]

        def topic_to_topology(self, topic):
            """
            Decode MQTT topic segments implementing the »quadruple hierarchy strategy«.

            The topology hierarchy is directly specified by the MQTT topic and is
            made up of a minimum of four identifiers describing the core structure::

                realm / network / gateway / node

            The topology identifiers are specified as:

                - "realm" is the designated root realm. You should prefix the topic name
                  with this label when opting in for all features of the telemetry platform.
                  For other purposes, feel free to publish to any MQTT topic you like.

                - "network" is your personal realm. Choose anything you like or use an
                  `Online GUID Generator <https://www.guidgenerator.com/>`_ to gain
                  maximum uniqueness.

                - "gateway" is your gateway identifier. Choose anything you like.
                  This does not have to be very unique, so you might use labels
                  having the names of sites. While you are the owner of this
                  namespace hierarchy, remember these labels might be visible on
                  the collaborative ether, though.
                  So the best thing would be to give kind of nicknames to your
                  sites which don't identify their location.

                - "node" is your node identifier. Choose anything you like. This usually
                  gets transmitted from an embedded device node. Remember one device node
                  might have multiple sensors attached, which is beyond the scope of the
                  collection platform: We just accept bunches of named measurement values,
                  no matter which sensors they might originate from.
                  In other words: We don't need nor favor numeric sensor identifiers,
                  let's give them names!
            """

            # regular expression pattern for decoding MQTT topic address segments
            pattern = r'^(?P<realm>.+?)/(?P<network>.+?)/(?P<gateway>.+?)/(?P<node>.+?)(?:/(?P<kind>.+?))?$'

            # decode the topic
            p = re.compile(pattern)
            m = p.match(topic)
            if m:
                address = Bunch(m.groupdict())
            else:
                address = {}

            return address


        def topology_to_database(self, topology):
            """
            Encode topology segment identifiers to database address.
            A database server usually has the concept of multiple databases, each with multiple tables.
            With other databases than RDBMS, they might be named differently, but the concept usually
            doesn't differ much.

            When mapping the topology quadruple (realm, network, gateway, node) in the form of:

                - realm + network = database name
                - gateway + node  = table name

            This fits perfectly to compute the slot where to store the measurements.
            """
            sanitize = self.sanitize_db_identifier
            database = Bunch({
                'database': '{}_{}'.format(sanitize(topology.realm), sanitize(topology.network)),
                'series':   '{}_{}'.format(sanitize(topology.gateway), sanitize(topology.node)),
            })
            return database


        @staticmethod
        def sanitize_db_identifier(value):
            """
            Better safe than sorry, databases accept different
            characters as database- or table names.
            """
            value = value.replace('/', '_').replace('.', '_').replace('-', '_')
            return value




Wishlist
========
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
