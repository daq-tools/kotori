##############
Setup on macOS
##############

Auxiliary services can be installed and run either natively
on macOS through Homebrew or by using Docker.


******
Native
******

Setup packages::

    brew install mosquitto influxdb grafana

See how daemons can be started::

    brew info mosquitto influxdb grafana | grep Caveats -A8brew info mosquitto influxdb grafana

It's basically::

    $ mosquitto
    $ influxdb
    $ grafana-server --config=/usr/local/etc/grafana/grafana.ini --homepath /usr/local/share/grafana cfg:default.paths.logs=/usr/local/var/log/grafana cfg:default.paths.data=/usr/local/var/lib/grafana cfg:default.paths.plugins=/usr/local/var/lib/grafana/plugins


******
Docker
******

Please have a look at :ref:`setup-docker` in order to get the
complementing services up and running using Docker.
