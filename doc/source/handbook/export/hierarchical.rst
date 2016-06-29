.. include:: ../../_resources.rst

.. highlight:: bash

.. _export-hierarchical-data:

########################
Hierarchical data export
########################
Kotori supports exporting data in HDF5_ and NetCDF_ formats.
Read some guidelines about obtaining and working with them.

HDF5
====
Download HDF5 file::

    export HTTP_URI=http://localhost:24642
    export MQTT_TOPIC=mqttkit-1/testdrive/area-42/node-2

    http GET $HTTP_URI/api/$MQTT_TOPIC/data.hdf5 --download

    Downloading to "testdrive_area_42_node_2_20160617T134041_20160627T134041.hdf5"
    Done. 583.78 kB in 0.00448s (127.14 MB/s)


Pre-flight checks::

    export HDF5FILE='testdrive_area_42_node_2_20160617T134041_20160627T134041.hdf5'
    file --brief $HDF5FILE
    Hierarchical Data Format (version 5) data

Install hdf5 and h5utils::

    sudo port install hdf5 h5utils

Inspect file with HDF5 tools::

    h5ls $HDF5FILE
    testdrive_area_42_node_2 Group

    h5ls --recursive $HDF5FILE
    /                        Group
    /testdrive_area_42_node_2 Group
    /testdrive_area_42_node_2/table Dataset {10403/Inf}

    h5dump --contents $HDF5FILE
    HDF5 "testdrive_area_42_node_2_20160617T134041_20160627T134041.hdf5" {
    FILE_CONTENTS {
     group      /
     group      /testdrive_area_42_node_2
     dataset    /testdrive_area_42_node_2/table
     }
    }

    h5dump --header $HDF5FILE
    [...]

    h5dump --group /testdrive_area_42_node_2 $HDF5FILE
    [...]

    h5dump --dataset /testdrive_area_42_node_2/table $HDF5FILE
    [...]

    h5stat $HDF5FILE
    [...]


Inspect file with PyTables_ tools::

    ptdump $HDF5FILE
    / (RootGroup) ''
    /testdrive_area_42_node_2 (Group) ''
    /testdrive_area_42_node_2/table (Table(10403,)) ''

    ptdump --showattrs $HDF5FILE
    / (RootGroup) ''
      /._v_attrs (AttributeSet), 0 attributes
    /testdrive_area_42_node_2 (Group) ''
      /testdrive_area_42_node_2._v_attrs (AttributeSet), 15 attributes:
       [CLASS := 'GROUP',
        TITLE := '',
        VERSION := '1.0',
        data_columns := [u'hour', u'month', u'second', u'day', u'minute'],
        encoding := None,
        index_cols := [(0, 'index')],
        info := {1: {'type': 'Index', 'names': [None]}, 'index': {'index_name': 'time'}},
        levels := 1,
        metadata := [],
        nan_rep := 'nan',
        non_index_axes := [(1, [u'hour', u'month', u'second', u'day', u'minute'])],
        pandas_type := 'frame_table',
        pandas_version := '0.15.2',
        table_type := 'appendable_frame',
        values_cols := [u'hour', u'month', u'second', u'day', u'minute']]
    /testdrive_area_42_node_2/table (Table(10403,)) ''


    ptdump --verbose $HDF5FILE
    / (RootGroup) ''
    /testdrive_area_42_node_2 (Group) ''
    /testdrive_area_42_node_2/table (Table(10403,)) ''
      description := {
      "index": Int64Col(shape=(), dflt=0, pos=0),
      "hour": Int64Col(shape=(), dflt=0, pos=1),
      "month": Int64Col(shape=(), dflt=0, pos=2),
      "second": Int64Col(shape=(), dflt=0, pos=3),
      "day": Int64Col(shape=(), dflt=0, pos=4),
      "minute": Int64Col(shape=(), dflt=0, pos=5)}
      byteorder := 'little'
      chunkshape := (1365,)


    ptdump --showattrs --dump $HDF5FILE
    [...]



.. note::

    Panoply_ can read a number of different hierarchical data
    formats and HDFView_ is a Java browser for HDF4 and HDF5 files.



NetCDF
======
Download NetCDF file::

    export HTTP_URI=http://localhost:24642
    export MQTT_TOPIC=mqttkit-1/testdrive/area-42/node-2

    http GET $HTTP_URI/api/$MQTT_TOPIC/data.nc --download

    Downloading to "testdrive_area_42_node_2_20160617T135522_20160627T135522.nc"
    Done. 583.78 kB in 0.00448s (127.14 MB/s)


Pre-flight checks::

    export NCFILE='testdrive_area_42_node_2_20160617T135522_20160627T135522.nc'
    file --brief $NCFILE
    Hierarchical Data Format (version 5) data

Install NetCDF tools::

    sudo port install netcdf

Inspect file with NetCDF tools::

    ncinfo $NCFILE
    <type 'netCDF4._netCDF4.Dataset'>
    root group (NETCDF4 data model, file format UNDEFINED):
        dimensions(sizes):
        variables(dimensions):
        groups: testdrive_area_42_node_2


    ncdump $NCFILE
    [...]

