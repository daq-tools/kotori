<?php
// -*- coding: utf-8 -*-
// (c) 2016-2019 Andreas Motl <andreas.motl@getkotori.org>
/*
========================================
Kotori telemetry client for PHP5 to PHP7
========================================

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
        "http://kotori.example.org/api",
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
    $telemetry = new TelemetryClient("http://kotori.example.org/api/mqttkit-1/testdrive/area-42/node-1/data");

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

            $result = http_get_contents($this->uri, $options);

            if ($result === FALSE) {
                error_log("Could not submit telemetry data to '{$this->uri}', payload='{$payload}'");
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

    function http_get_contents($url, $stream_options) {

        $curl = curl_init($url);

        $options = $stream_options['http'];
        $ssl_options = $stream_options['ssl'];

        if (isset($ssl_options['verify_peer'])) {
            curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, $ssl_options['verify_peer']);
        }
        if ($options['header']) {
            curl_setopt($curl, CURLOPT_HTTPHEADER, explode("\r\n", $options['header']));
        }
        if ($options['method'] == 'POST') {
            curl_setopt($curl, CURLOPT_POST, true);
        }
        if ($options['content']) {
            curl_setopt($curl, CURLOPT_POSTFIELDS, $options['content']);
        }
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);

        $response = curl_exec($curl);

        // Check and output error message, if any
        $error_message = curl_error($curl);
        if ($error_message) {
            trigger_error($error_message, E_USER_WARNING);
        }

        curl_close($curl);

        return $response;

    }

}

?>
