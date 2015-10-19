======================
Kotori Hiveeyes README
======================

Start Kotori DAQ
================

Run interactively::

    ssh kotori@elbanco.hiveeyes.org
    source ~/develop/kotori-daq/.venv27/bin/activate
    kotori --config ~/develop/kotori-daq/etc/hiveeyes.ini --debug


Run in tmux session::

    ssh kotori@elbanco.hiveeyes.org
    tmux new -s kotori 'bash -c "source ~/develop/kotori-daq/.venv27/bin/activate; kotori --config ~/develop/kotori-daq/etc/hiveeyes.ini --debug; exec bash"'


Attach to running Kotori DAQ
============================
::

    ssh kotori@elbanco.hiveeyes.org
    tmux att -t kotori


URL entrypoints
===============

- | InfluxDB UI
  | http://swarm.hiveeyes.org:8083/
- | InfluxDB API
  | http://swarm.hiveeyes.org:8086/
- | Grafana
  | http://swarm.hiveeyes.org:3000/


Serial to MQTT forwarding
=========================

publish message::

    $ cd mqtt-to-serial
    $ make pretend   # make pretend-swarm
    publish: hiveeyes/100/1/99/temp1 2218
    publish: hiveeyes/100/1/99/temp2 2318
    publish: hiveeyes/100/1/99/temp3 2462
    publish: hiveeyes/100/1/99/temp4 2250
    publish: hiveeyes/100/1/99/message-bencode li100ei99ei1ei2218ei2318ei2462ei2250ee
    publish: hiveeyes/100/1/99/message-json {"network_id": 100, "node_id": 99, "gateway_id": 1, "temp1": 2218, "temp2": 2318, "temp3": 2462, "temp4": 2250}


InfluxDB authentication
=======================

https://influxdb.com/docs/v0.9/administration/authentication_and_authorization.html#set-up-authentication

create admin user::

     $ curl --silent --get 'http://swarm.hiveeyes.org:8086/query?pretty=true' --user root:root --data-urlencode 'q=CREATE USER admin WITH PASSWORD 'Armoojwi' WITH ALL PRIVILEGES'




InfluxDB querying
=================

list databases::

     $ curl --silent --get 'http://swarm.hiveeyes.org:8086/query?pretty=true' --user admin:Armoojwi --data-urlencode 'q=SHOW DATABASES' | jq '.'

query influxdb::

    $ curl --silent --get 'http://swarm.hiveeyes.org:8086/query?pretty=true' --user admin:Armoojwi --data-urlencode 'db=hiveeyes_999' --data-urlencode 'q=select * from "1.99";' | jq '.'
    [
      {
        "name": "1.99",
        "columns": [
          "time",
          "sequence_number",
          "temp1",
          "temp4",
          "temp3",
          "temp2"
        ],
        "points": [
          [
            1445091695268,
            159830001,
            2218,
            2250,
            2462,
            2318
          ]
        ]
      }
    ]
