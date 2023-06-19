(databases)=
(kotori-databases)=
# Databases

Database adapter components will know about vendor-specific dialects and optimal
communication strategies to timeseries-databases.

This documentation section enumerates the collection of database adapters shipped
with Kotori. Adding more adapters is possible.


```{toctree}
:caption: Databases
:maxdepth: 1
:hidden:

influxdb
mongodb
```


::::::{grid} 1
:margin: 0
:padding: 0


:::::{grid-item-card}
::::{grid} 2
:margin: 0
:padding: 0

:::{grid-item}
:columns: 8
#### [](#database-influxdb)

InfluxDB is a scalable datastore and time series platform for metrics, events,
and real-time analytics. It covers storing and querying data, background ETL processing
for monitoring and alerting purposes, and visualization and exploration features. 

<small>
<strong>Categories:</strong> timeseries-database
</small>
:::
:::{grid-item}
:columns: 4
{bdg-primary-line}`eth` {bdg-primary-line}`wifi` {bdg-primary-line}`http`

{bdg-success-line}`ilp` {bdg-success-line}`influxql` {bdg-success-line}`flux` 

{bdg-secondary-line}`amd64` {bdg-secondary-line}`arm64`
:::
::::
:::::


:::::{grid-item-card}
::::{grid} 2
:margin: 0
:padding: 0

:::{grid-item}
:columns: 8
#### [](#database-mongodb)

MongoDB is a document database designed for ease of application development and scaling.

<small>
<strong>Categories:</strong> document-database
</small>
:::
:::{grid-item}
:columns: 4
{bdg-primary-line}`eth` {bdg-primary-line}`wifi` {bdg-primary-line}`http`

{bdg-success-line}`json` {bdg-success-line}`bson` 

{bdg-secondary-line}`amd64` {bdg-secondary-line}`arm64`
:::
::::
:::::


::::::
