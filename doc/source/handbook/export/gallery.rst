.. include:: ../../_resources.rst

.. _data-export-gallery:

#######################
Gallery of data exports
#######################

A weight-loss event from monitoring a beehive on May 19, 2016, plotted using matplotlib:

.. figure:: https://swarm.hiveeyes.org/api/hiveeyes/25a0e5df-9517-405b-ab14-cb5b514ac9e8/3756782252718325761/1/data.png?include=wght2&from=20160519T040000&to=20160519T170000
    :alt: A weight-loss event from monitoring a beehive on May 19, 2016; plotted using matplotlib
    :width: 500px
    :align: left
    :figclass: caption-regular

    Weight-loss plot using matplotlib

.. figure:: https://swarm.hiveeyes.org/api/hiveeyes/25a0e5df-9517-405b-ab14-cb5b514ac9e8/3756782252718325761/1/data.png?include=wght2&from=20160519T040000&to=20160519T170000&renderer=ggplot
    :alt: A weight-loss event from monitoring a beehive on May 19, 2016; plotted using ggplot
    :width: 500px
    :align: right
    :figclass: caption-regular

    Weight-loss plot using ggplot

|clearfix|


****
TODO
****

- http://localhost:24642/api/hiveeyes/25a0e5df-9517-405b-ab14-cb5b514ac9e8/3756782252718325761/1/data.png?exclude=wght1,RSSI1,rACK1&from=20160519T040000&to=20160519T170000&pad=true
- http://localhost:24642/api/hiveeyes/25a0e5df-9517-405b-ab14-cb5b514ac9e8/3756782252718325761/1/data.png?exclude=wght1,RSSI1,rACK1&from=20160519T040000&to=20160519T170000&pad=true
- http://localhost:24642/api/hiveeyes/25a0e5df-9517-405b-ab14-cb5b514ac9e8/3756782252718325761/1/data.png?include=wght2&from=20160519T040000&to=20160519T170000&pad=true

::

    include, exclude, pad
    interpolate=true
    &from=20160519
    sorted

