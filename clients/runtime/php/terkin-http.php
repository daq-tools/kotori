<?php
// -*- coding: utf-8 -*-
// (c) 2016 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
/*
===============================
Kotori telemetry client for PHP
===============================

Documentation
-------------
https://getkotori.org/docs/handbook/acquisition/runtime/php.html#library


Synopsis
--------
Transmit telemetry data from PHP::

    // Put this file into the folder of your PHP program
    include("terkin-http.php");

    // Acquire HTTP API library
    use Terkin\TelemetryNode;

    // Create a "Node API" telemetry client object
    $telemetry = new TelemetryNode(
        "http://kotori.example.org/api/bus/mqtt",
        array(
            "realm"     => "mqttkit-1",
            "network"   => "testdrive",
            "gateway"   => "area-42",
            "node"      => "node-1",
        )
    );

    // Transmit data
    $data = array("temperature" => 42.84, "humidity" => 83);
    $telemetry->transmit($data);


Basic API
---------

    // Create a "Basic API" telemetry client object
    use Terkin\TelemetryClient;
    $telemetry = new TelemetryClient("http://kotori.example.org/api/bus/mqtt/mqttkit-1/testdrive/area-42/node-1/data");

*/

namespace Terkin {

    class TelemetryClient {
        /***
         *
         * Telemetry data client: Basic API
         *
        **/

        function __construct($uri) {
            $this->uri = $uri;
        }

        function transmit($data) {
            /*
             * Submit telemetry data using HTTP POST request
             * Serialization: x-www-form-urlencoded
             */

            $payload = http_build_query($data);

            // Use key 'http' even if you send the request to https://...
            $options = array(
                'http' => array(
                    'header'  => "Content-type: application/x-www-form-urlencoded\r\n",
                    'method'  => 'POST',
                    'content' => $payload
                )
            );
            $context  = stream_context_create($options);
            $result = file_get_contents($this->uri, false, $context);
            if ($result === FALSE) {
                error_log("Could not submit telemetry data to '$uri', payload='$payload'");
            }

            return $result;
        }

    }

    class TelemetryNode {
        /***
         *
         * Telemetry node client: Network participant API
         *
        **/

        function __construct($api_uri, $options) {
            $this->api_uri = $api_uri;
            $this->realm   = $options['realm'];
            $this->network = $options['network'];
            $this->gateway = $options['gateway'];
            $this->node    = $options['node'];

            $this->channel_uri = "{$this->api_uri}/{$this->realm}/{$this->network}/{$this->gateway}/{$this->node}";
            echo 'Channel URI: ' . $this->channel_uri . "\n";

            $this->client = new TelemetryClient("{$this->channel_uri}/data");
        }

        function transmit($data) {
            return $this->client->transmit($data);
        }

    }

}

?>
