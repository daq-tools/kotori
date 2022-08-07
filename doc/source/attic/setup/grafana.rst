#################
Configure Grafana
#################


******************
Auto configuration
******************
Kotori automatically creates default dashboards in Grafana, on which you can build upon.
This is sweet.

.. tip:: For more information, please read the source. YMMV.


********************
Manual configuration
********************


Howtos
======
- http://docs.grafana.org/datasources/influxdb/


Configuration
=============

Access Grafana
--------------

Go to Grafana's web frontend:

- url:  http://daq.example.net:3000/
- user: admin
- pass: admin       # Grafana 3.x
- pass: secret      # Grafana 2.x



Add InfluxDB datasource
-----------------------
See also:
http://docs.grafana.org/datasources/influxdb/

- Base settings
    - URL: http://daq.example.net:3000/datasources/new
    - Name: Kotori Telemetry
    - Default: yes
    - Type: InfluxDB 0.8.x
- Http settings
    - Url: http://daq.example.net:8086/
    - Access: proxy
- InfluxDB Details
    - Database: kotori
    - User: root
    - Password: ROOT


Add Kotori dashboard
--------------------

Either manually:

    - Go to http://daq.example.net:3000/dashboard/new
    - Add Panel » Graph
    - Add metric fields

Or by importing:

    - http://daq.example.net:3000/dashboard/import
    - doc/grafana-kotori-dashboard.json


View Dashboard:

    - http://daq.example.net:3000/dashboard/db/kotori
