<?php
// -*- coding: utf-8 -*-
// (c) 2016 Andreas Motl <andreas.motl@getkotori.org>
/*
================================
Kotori telemetry client for PHP4
================================

Documentation
-------------
https://getkotori.org/docs/handbook/acquisition/runtime/php.html#library


Synopsis
--------
Transmit telemetry data from PHP::

    // Put this file into the folder of your PHP program
    include("terkin-http.php4");

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
    $telemetry = new TelemetryClient("http://kotori.example.org/api/mqttkit-1/testdrive/area-42/node-1/data");

*/

class TelemetryClient {
    /***
     *
     * Telemetry data client: Basic API
     *
    **/

    function TelemetryClient($uri) {
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
            ),
            'ssl' => array(
                'allow_self_signed' => true,

                // TODO: Let's check whether we should not _always_ disable certificate verification.
                'verify_peer' => false,
            ),
        );

        $result = http_get_contents($this->uri, $options);

        if ($result === FALSE) {
            trigger_error("Could not submit telemetry data to '$this->uri', payload='$payload'", E_USER_ERROR);
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

    function TelemetryNode($api_uri, $options) {
        $this->api_uri = $api_uri;
        $this->realm   = $options['realm'];
        $this->network = $options['network'];
        $this->gateway = $options['gateway'];
        $this->node    = $options['node'];

        $this->channel_uri = "{$this->api_uri}/{$this->realm}/{$this->network}/{$this->gateway}/{$this->node}";
        //print 'Channel URI: ' . $this->channel_uri . "\n";

        $this->client = new TelemetryClient("{$this->channel_uri}/data");
    }

    function transmit($data) {
        return $this->client->transmit($data);
    }

}

function http_get_contents($url, $stream_options) {

    $ch = curl_init($url);

    $options = $stream_options['http'];
    $ssl_options = $stream_options['ssl'];

    if (isset($ssl_options['verify_peer'])) {
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, $ssl_options['verify_peer']);
    }
    if ($options['header']) {
        curl_setopt($ch, CURLOPT_HTTPHEADER, split("\r\n", $options['header']));
    }
    if ($options['method'] == 'POST') {
        curl_setopt($ch, CURLOPT_POST, true);
    }
    if ($options['content']) {
        curl_setopt($ch, CURLOPT_POSTFIELDS, $options['content']);
    }
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

    $response = curl_exec($ch);

    // Check and output error message, if any
    $error_message = curl_error($ch);
    if ($error_message) {
        trigger_error($error_message, E_USER_WARNING);
    }

    curl_close($ch);

    return $response;

}

// Mitigate "Fatal error: Call to undefined function: http_build_query()" on PHP4
// http://tutorialspots.com/function-http_build_query-in-php4-215.html
if (!function_exists('http_build_query')) {
    function http_build_query($data, $prefix = null, $sep = '', $key = '') {
        $ret = array();
        foreach ((array )$data as $k => $v) {
            $k = urlencode($k);
            if (is_int($k) && $prefix != null) {
                $k = $prefix . $k;
            }

            if (!empty($key)) {
                $k = $key . "[" . $k . "]";
            }

            if (is_array($v) || is_object($v)) {
                array_push($ret, http_build_query($v, "", $sep, $k));
            } else {
                array_push($ret, $k . "=" . urlencode($v));
            }
        }

        if (empty($sep)) {
            $sep = ini_get("arg_separator.output");
        }

        return implode($sep, $ret);
    }
}

?>
