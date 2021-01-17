.. _processing-tags:

########################
Processing InfluxDB tags
########################

.. highlight:: python


********
Question
********

    - I already have data in my InfluxDB, but without tags.
      How could I add tags like ``latitude`` and ``longitude``?

    - Is the feature of adding tags to the InfluxDB database not implemented yet?


******
Answer
******
It well is - kind of. But you will have to resort to make changes
to the code if the behavior here does not cover your needs already.
Currently, the following ingress field names are automatically
processed as InfluxDB tags::

    tag_fields_main = ['geohash', 'latitude', 'longitude']
    tag_fields_more = ['location', 'location_id', 'location_name', 'sensor_id', 'sensor_type']

Source code
===========
If this doesn't fit, you might want to amend some code within
`kotori.daq.storage.influx.format_chunk`_ according to your needs.
The whole file is about the data acquisition path where you will
get an insight how data is actually written into the InfluxDB database.
Inside this method, you will find references to ``chunk["tags"]``,
which is a dictionary where you can stuff tags into.

Example
=======
There's already a section for `transforming the "geohash" telemetry field to an InfluxDB tag`_::

    # Extract geohash from data.
    # TODO: Also precompute geohash with 3-4 different zoomlevels and add them as tags.
    if "geohash" in data:
        chunk["tags"]["geohash"] = data["geohash"]
        del data['geohash']

Outlook
=======
.. todo::

    A mechanism to declare a set of static tags per channel by
    defining  them inside the Kotori configuration file would be nice.
    Please let us know if you see other mechanisms for injecting
    tags into the record here.


----


********
Question
********

    So I can just add additional tags within `influx.py#L145 <https://github.com/daq-tools/kotori/blob/0.22.7/kotori/daq/storage/influx.py#L145>`_?

******
Answer
******
Correct, you can fill key/value pairs into ``chunk["tags"]`` anywhere within this method.
Whether you statically insert them right there using a hacked version of ``influx.py`` or
if you want to derive the tag fields from the data ingress payload itself like seen with
the fields ``geohash``, ``location``, ``location_id``, ``location_name``, ``sensor_id``
and ``sensor_type`` is really up to you.


----


********
Question
********

    I can't find and edit the ``influx.py`` script on my machine.

******
Answer
******
When installing Kotori from the Debian package, it will unfold
at e.g. ``/opt/kotori/lib/python3.8/site-packages/kotori``.

.. attention::

    Please note when making changes to the files within this directory,
    they will be overwritten when installing a new version of Kotori
    from the package repositories.

    So, take care of your amendments or better send them upstream to
    us in order to become part of the software.


----


**********
References
**********
- https://github.com/daq-tools/kotori/issues/14


.. _kotori.daq.storage.influx.format_chunk: https://github.com/daq-tools/kotori/blob/0.22.7/kotori/daq/storage/influx.py#L125-L231
.. _transforming the "geohash" telemetry field to an InfluxDB tag: https://github.com/daq-tools/kotori/blob/0.22.7/kotori/daq/storage/influx.py#L181-L191
