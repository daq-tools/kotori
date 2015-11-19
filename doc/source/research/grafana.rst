================
Grafana Research
================

Sub second resolution
---------------------
- https://github.com/grafana/grafana/issues/714
- https://github.com/grafana/grafana/issues/720
- https://github.com/grafana/grafana/issues/728
- https://github.com/grafana/grafana/pull/752
- | InfluxDB: Support for sub second resolution graphs
  | https://github.com/grafana/grafana/commit/ebcf2c3f6854cbe2903ad8c97af18018c5b42c7b
- http://192.168.59.103:3000/api/datasources/proxy/14/query?epoch=ms&q=SELECT+derivative(wght1)+FROM+%22tug22_999%22+WHERE+time+%3E+1447538527s+and+time+%3C+1447538528s+GROUP+BY+time(100ms)

More info
- https://influxdb.com/docs/v0.9/troubleshooting/frequently_encountered_issues.html#identifying-write-precision-from-returned-timestamps
- https://influxdb.com/docs/v0.8/api/reading_and_writing_data.html

Misc
----
- http://www.rittmanmead.com/2015/02/obiee-monitoring-and-diagnostics-with-influxdb-and-grafana/
- https://pypi.python.org/pypi/grafana_alerts
- https://pypi.python.org/pypi/grafana_api_client
- https://pypi.python.org/pypi/grafyaml
- https://pypi.python.org/pypi/grafcli
- https://github.com/m110/grafcli
- https://github.com/m110/climb
- https://pypi.python.org/pypi/monasca-ui
- https://github.com/openstack/horizon
- http://docs.grafana.org/guides/gettingstarted/
- https://www.youtube.com/watch?v=sKNZMtoSHN4&index=7&list=PLDGkOdUX1Ujo3wHw9-z5Vo12YLqXRjzg2
