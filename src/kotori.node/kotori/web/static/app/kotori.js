// -*- coding: utf-8 -*-
/*
 (c) 2014-2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
 derived from https://github.com/tavendo/AutobahnPython/blob/master/examples/twisted/wamp/pubsub/simple/example2/index.html
 */

// When rending an underscore template, we want top-level
// variables to be referenced as part of an object. For
// technical reasons (scope-chain search), this speeds up
// rendering; however, more importantly, this also allows our
// templates to look / feel more like our server-side
// templates that use the rc (Request Context / Colletion) in
// order to render their markup.
// http://www.bennadel.com/blog/2411-Using-Underscore-js-Templates-To-Render-HTML-Partials.htm
_.templateSettings.variable = "rc";

// X-editable: turn to inline mode
$.fn.editable.defaults.mode = 'inline';

// Grab the HTML out of our template tag and pre-compile it.
var node_template = _.template(
    $("#node-template").html()
);

// WAMP session object
var sess;
var nodes_ui = {};

// data sink for udp adapter
var ringbuffer_size = 100;
var telemetry_graph = {
    'mma_x': [],
    'mma_y': [],
    'temp': [],
};
var telemetry = {
    'mma_x': new CBuffer(ringbuffer_size),
    'mma_y': new CBuffer(ringbuffer_size),
    'temp': new CBuffer(ringbuffer_size),
};
var graph;

var map;
var marker;

window.onload = function() {



    // ------------------------------------------
    //   realtime Map powered by leaflet
    // ------------------------------------------

    L.Icon.Default.imagePath = 'static/img';

	map = L.map('map').setView([51.505, -0.09], 13);

	L.tileLayer('https://{s}.tiles.mapbox.com/v3/{id}/{z}/{x}/{y}.png', {
    		attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery &copy; <a href="http://mapbox.com">Mapbox</a>',
		id: 'examples.map-i875mjb7',
   	 	maxZoom: 18
	}).addTo(map);

	marker = L.marker([51.5, -0.09]).addTo(map);


    // ------------------------------------------
    //   telemetry timeseries graph
    // ------------------------------------------
    var palette = new Rickshaw.Color.Palette( { scheme: '' } );
    graph = new Rickshaw.Graph( {
        element: document.querySelector("#chart"),
        renderer: 'line',
        width: 800,
        height: 300,
        series: [
            {
                color: palette.color(),
                data: telemetry_graph['mma_x'],
            },
            {
                color: palette.color(),
                data: telemetry_graph['mma_y'],
            },
            {
                color: palette.color(),
                data: telemetry_graph['temp'],
            },
        ]
    });
    graph.render();


    // websocket url defaults
    wsuri = "ws://" + window.location.hostname + ":9000/ws";
    /*
    if (!wsuri) {
        if (window.location.protocol === "file:") {
            wsuri = "ws://localhost:9000/ws";

        } else {
            wsuri = "ws://" + window.location.hostname + ":9000/ws";
        }
    }
    */

    // explicitly specified websocket url
    var url = $.url(window.location.href);
    var master_uri = url.param('master');
    if (master_uri) wsuri = master_uri;

    console.log('[WAMP] INFO: Connecting to ' + wsuri);

    //ab.debug(true, true, true);

    // connect to WAMP server
    var connection = new autobahn.Connection({
        url: wsuri,
        realm: 'kotori-realm'
    });

    // WAMP session was established
    connection.onopen = function (session) {

        sess = session;
        console.log("Connected!");


        /*
        sess.prefix("registry", "http://kotori.elmyra.de/registry#");
        sess.prefix("broadcast", "de.elmyra.kotori.broadcast");
        sess.prefix("dashboard", "http://kotori.elmyra.de/dashboard#");
        */

        sess.prefix("registry",  "de.elmyra.kotori.registry");
        sess.prefix("broadcast", "de.elmyra.kotori.broadcast");
        sess.prefix("telemetry", "de.elmyra.kotori.telemetry");
        sess.prefix("dashboard", "de.elmyra.kotori.dashboard");

        gui_init();

        sess.subscribe("broadcast:heartbeat", node_heartbeat);
        //sess.subscribe("broadcast:node-activity", dump_event);
        sess.subscribe("broadcast:node-activity", node_state);
        sess.subscribe("broadcast:node-privacy", node_state);
        sess.subscribe("telemetry:data", node_data);
        sess.subscribe("broadcast:operator-presence", dump_event);
        sess.subscribe("dashboard:update", dashboard_update);

        // trigger dashboard update
        sess.publish("dashboard:update", null, false);

        //session.call('com.timeservice.now').then(session.log);

        /*
         session.publish('broadcast:heartbeat', ['abc', 'def']);
         window.setInterval(function() {
         console.log('publish from javascript');
         //session.publish('broadcast:heartbeat', ['abc', 'def']);
         session.publish('broadcast:heartbeat', ['abc', 'def']);
         }, 60000);
         console.log('YEAH!');
         return;
         */

    }

    // WAMP session is gone
    //function(code, reason) {
    connection.onclose = function (evt, reason) {
        console.log('[WAMP] Closing session. event:', evt, 'reason:', reason);
        //console.log('[WAMP] ERROR: ' + 'code: ' + code + ', reason: ' + reason);
        //sess = null;
        //alert(reason);
        //dashboard_clear();
    }

    connection.open();

};


// receive UDP data here
function node_data(data) {

    //console.log('data:', data);

    // display raw telemtry data
    var data_display = data;
    if (_.isObject(data)) {
        data_display = JSON.stringify(data_display);
    }
    $('#telemetry-content').prepend(data_display, '<br/>');



    // add data point to timeseries graph
    var values = data[0].split(';');
    var mma_x = values[0];
    var mma_y = values[1];
    var temp = values[2];

    try {
        var lat = values[3];
        var lng = values[4];

        var latlng = L.latLng(parseFloat(lat), parseFloat(lng));
        //map.panTo(latlng);
        marker.setLatLng(latlng);
        marker.update();

    } catch (ex) {
        console.warn('Could not decode GPS position:', ex);

    }



    var now = new Date().getTime();
    //console.log(mma_x, mma_y);
    //console.log({ x: now, y: parseFloat(mma_x) });
    telemetry['mma_x'].push({ x: now, y: parseFloat(mma_x) });
    telemetry['mma_y'].push({ x: now, y: parseFloat(mma_y) });
    telemetry['temp'].push({ x: now, y: parseFloat(temp) });

    //console.log(telemetry['mma_x'].data);

    telemetry_graph['mma_x'].splice(0, telemetry_graph['mma_x'].length);
    telemetry['mma_x'].toArray().forEach(function(v) {telemetry_graph['mma_x'].push(v)}, this);

    telemetry_graph['mma_y'].splice(0, telemetry_graph['mma_y'].length);
    telemetry['mma_y'].toArray().forEach(function(v) {telemetry_graph['mma_y'].push(v)}, this);

    telemetry_graph['temp'].splice(0, telemetry_graph['temp'].length);
    telemetry['temp'].toArray().forEach(function(v) {telemetry_graph['temp'].push(v)}, this);

    graph.update();

}



function gui_init() {

    // operator presence
    $('#operator-presence').on('click', function() {
        var btn = this;
        setTimeout(function() {
            var presence = $(btn).hasClass('active');
            console.log('presence:', presence);
            sess.publish("broadcast:operator-presence", [presence, false]);
            //sess.call("broadcast:operator-presence", [presence, false]);

        });
    });

    $('#telemetry-clear').on('click', function() {
        $('#telemetry-content').empty();
    });
}

function dump_event(topic, event) {
    console.log({'topic': topic, 'event': event});
}

function node_heartbeat(topic, node_id) {
    console.log('node_heartbeat');
    console.log({'topic': topic, 'node_id': node_id});
}

function node_state(topic, event) {
    var node_id = event.node_id;
    var state = event.state;
    console.log({'topic': topic, 'node_id': node_id, 'state': state});

    var topic_url = $.url(topic);
    var topic_short = topic_url.attr('fragment');

    // show activity indicator
    if (topic_short == 'node-activity') {
        if (state) {
            $('#activity-' + node_id).show();
        } else {
            $('#activity-' + node_id).hide();
        }
    } else if (topic_short == 'node-privacy') {
        if (state) {
            $('#privacy-' + node_id).show();
        } else {
            $('#privacy-' + node_id).hide();
        }
    }
}

function dashboard_clear() {
    $("#item-container").empty();
}

function node_online(node_id) {
    $('#online-' + node_id).show();
    $('#offline-' + node_id).hide();
}

function node_offline(node_id) {
    $('#online-' + node_id).hide();
    $('#offline-' + node_id).show();
}

function dashboard_update(topic, event) {

    sess.call("registry:get_nodes").then(function(nodes_registry) {
        ab.log('nodes_registry:', nodes_registry);

        //dashboard_clear();

        $.each(nodes_registry, function(node_id, node_info) {

            if (node_id in nodes_ui) {
                return;
            }
            nodes_ui[node_id] = true;

            var template_data = {node_id: node_id, node_hostname: node_info['hostname'], node_label: node_info['label'] || node_id};
            var node_html = node_template(template_data);
            //console.log(node_html);
            $("#item-container").append(node_html);

            // initialize behaviours

            // text-to-speech input field: submit text on enter
            var tts_listener = function(node_id, text_element) {
                return function(e) {
                    var code = e.keyCode || e.which;
                    if (code == 13) {
                        e.preventDefault();
                        sayText(node_id, $(text_element).val())
                        //return false;
                    }
                }
            }
            var tts_input = '#tts-' + node_id;
            $(tts_input).bind('keypress', tts_listener(node_id, tts_input));

            // various indicators: switch from bootstrap hiding to jQuery hiding
            // https://stackoverflow.com/questions/18568736/how-to-hide-element-using-twitter-bootstrap-3-and-show-it-using-jquery/20529829#20529829
            $('#online-' + node_id).hide().removeClass('hide');
            $('#offline-' + node_id).hide().removeClass('hide');
            $('#activity-' + node_id).hide().removeClass('hide');
            $('#privacy-' + node_id).hide().removeClass('hide');

            // setup editable fields
            $('#node-label-' + node_id).editable({
                type: 'text',
                success: function(response, value) {
                    //userModel.set('username', value); //update backbone model
                    sess.call("registry:set_node_label", node_id, value);
                    console.log('edit:', node_id, value);
                }
            });

        });

        // indicate node online/offline state
        $.each(nodes_ui, function(node_id, state) {
            //console.log(node_id);
            if (node_id in nodes_registry) {
                node_online(node_id);
            } else {
                nodes_ui[node_id] = false;
                node_offline(node_id);
            }
        });


        /*
        var node_select = document.getElementById("node_id-0");
        node_select.options.length = 0;
        for (index in nodelist) {
            var node_id = nodelist[index];
            node_select.options[node_select.options.length] = new Option(node_id, node_id);
        }
        */
    });
}



function sayText(node_id, message) {
    /*
    evt = {};
    evt.node_id = node_id;
    evt.message = message;
    evt.date = new Date();
    */

    if (!sess) {
        console.error('ERROR: No WAMP session with Kotori master service');
        return;
    }

    var node_topic = 'http://kotori.elmyra.de/node/' + node_id + '#';
    sess.prefix(node_id, node_topic);
    //sess.subscribe(node_topic, dump_event);
    var event_topic = node_id + ':say';
    console.log('publishing: ' + event_topic + ' ' + message)
    sess.publish(event_topic, message);
}
