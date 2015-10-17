publish message::

    $ cd mqtt-to-serial
    $ make fake
    publish: hiveeyes/100/1/99/temp1 2218
    publish: hiveeyes/100/1/99/temp2 2318
    publish: hiveeyes/100/1/99/temp3 2462
    publish: hiveeyes/100/1/99/temp4 2250
    publish: hiveeyes/100/1/99/message-bencode li100ei99ei1ei2218ei2318ei2462ei2250ee
    publish: hiveeyes/100/1/99/message-json {"network_id": 100, "node_id": 99, "gateway_id": 1, "temp1": 2218, "temp2": 2318, "temp3": 2462, "temp4": 2250}


query influxdb::

    $ curl --silent --get 'http://192.168.59.103:8086/db/hiveeyes.100/series?u=root&p=root' --data-urlencode 'q=select * from "1.99";' | jq '.'
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
