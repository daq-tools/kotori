.. _daq-javascript:
.. _daq-typescript:

#####################
JavaScript/TypeScript
#####################


*****
About
*****
Terkin Telemetry client library for JavaScript, written in TypeScript.
See https://github.com/daq-tools/terkin-javascript.

Terkin is a client-side library, framework and concept for
signalling telemetry data within nodes of a sensor network.


********
Synopsis
********

.. highlight:: javascript

::

    var terkin = require('./terkin');

    var telemetry_node = new terkin.TelemetryNode(
        "https://daq.example.org/api",
        {
            "realm": "mqttkit-1",
            "network": "testdrive",
            "gateway": "terkin",
            "node": "js-node-01",
        }
    );

    var data = {"temperature": 42.84, "humidity": 83.01};
    telemetry_node.transmit(data);
