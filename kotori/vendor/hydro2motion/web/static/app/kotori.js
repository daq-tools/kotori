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
var lat;
var lng;
var legend;
var polyline;

// data sink for udp adapter
var ringbuffer_size = 240;
var telemetry_graph = {
    'V_FC': [],
    'V_CAP': [],
    'A_ENG': [],
    'A_CAP': [],
    'T_Air_in': [],
    'T_Air_out': [],
    'T_FC_H2O_out': [],
    'Water_in': [],
    'Water_out': [],
    'Drive_SW': [],
    'H2_flow': [],
    'GPS_Speed': [],
    'V_Safety': [],
};
var telemetry = {
    'V_FC': new CBuffer(ringbuffer_size),
    'V_CAP': new CBuffer(ringbuffer_size),
    'A_ENG': new CBuffer(ringbuffer_size),
    'A_CAP': new CBuffer(ringbuffer_size),
    'T_Air_in': new CBuffer(ringbuffer_size),
    'T_Air_out': new CBuffer(ringbuffer_size),
    'T_FC_H2O_out': new CBuffer(ringbuffer_size),
    'Water_in': new CBuffer(ringbuffer_size),
    'Water_out': new CBuffer(ringbuffer_size),
    'Drive_SW': new CBuffer(ringbuffer_size),
    'H2_flow': new CBuffer(ringbuffer_size),
    'GPS_Speed': new CBuffer(ringbuffer_size),
    'V_Safety': new CBuffer(ringbuffer_size),
};
var graph;

var map;
var marker;

window.onload = function() {

    // ------------------------------------------
    //   realtime Map powered by leaflet
    // ------------------------------------------

    L.Icon.Default.imagePath = 'static/img';

	map = L.map('map').setView([51.882804, 4.488303], 16);

	L.tileLayer('https://{s}.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiYmFzdGlhbmhlbm5la2UiLCJhIjoiczZLeUpYbyJ9.01Znhen2le-PF6G4307P9Q', {
    		attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery &copy; <a href="http://mapbox.com">Mapbox</a>',
		id: 'bastianhenneke.m565ad47',
   	 	maxZoom: 18
	}).addTo(map);

	var polylinePoints = [
            new L.LatLng(51.882804, 4.488303),
            new L.LatLng(51.883645, 4.488357),
			];

	marker = L.marker([51.882804, 4.488303]).addTo(map);
	polyline =	L.polyline(polylinePoints, {color: 'green'}).addTo(map);

    // ------------------------------------------
    //   telemetry timeseries graph
    // ------------------------------------------
    var palette = new Rickshaw.Color.Palette( { scheme: '' } );
    graph = new Rickshaw.Graph( {
        element: document.querySelector("#chart"),
        renderer: 'line',
        width: 680,
        height: 300,
        series: [
            {
                name: "V_FC",
		color: palette.color(),
                data: telemetry_graph['V_FC'],
            },
            {
                name: "V_CAP",
		color: palette.color(),
                data: telemetry_graph['V_CAP'],
            },
            {
                name: "A_ENG",
		color: palette.color(),
                data: telemetry_graph['A_ENG'],
            },
	    {
                name: "A_CAP",
		color: palette.color(),
                data: telemetry_graph['A_CAP'],
            },
	    {
                name: "T_Air_in",
		color: palette.color(),
                data: telemetry_graph['T_Air_in'],
            },
	    {
                name: "T_Air_out",
		color: palette.color(),
                data: telemetry_graph['T_Air_out'],
            },
	    {
                name: "T_FC_H2O_out",
		color: palette.color(),
                data: telemetry_graph['T_FC_H2O_out'],
            },
	    {
                name: "Water_in",
		color: palette.color(),
                data: telemetry_graph['Water_in'],
            },
	    {
                name: "Water_out",
		color: palette.color(),
                data: telemetry_graph['Water_out'],
            },
	    {
                name: "Drive_SW",
		color: palette.color(),
                data: telemetry_graph['Drive_SW'],
            },
	    {
                name: "H2_flow",
		color: palette.color(),
                data: telemetry_graph['H2_flow'],
            },
	    {
                name: "GPS_Speed",
		color: palette.color(),
                data: telemetry_graph['GPS_Speed'],
            },
	    {
                name: "V_Safety",
		color: palette.color(),
                data: telemetry_graph['V_Safety'],
            },

        ]
    });

    var y_axis = new Rickshaw.Graph.Axis.Y( {
        graph: graph,
        orientation: 'left',
        tickFormat: Rickshaw.Fixtures.Number.formatKMBT,
        element: document.getElementById('y_axis'),
    } );

    var legend = new Rickshaw.Graph.Legend( {
    	element: document.querySelector('#legend'),
        graph: graph
    } );

    var shelving = new Rickshaw.Graph.Behavior.Series.Toggle({
    graph: graph,
    legend: legend
    });

    var highlighter = new Rickshaw.Graph.Behavior.Series.Highlight({
    graph: graph,
    legend: legend
    });

    graph.render();


    // websocket url defaults
    wsuri = "ws://lablab.cicer.de:9000/ws";
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
   



    // add data point to timeseries graph
    var values = data[0].split(';');
    var V_FC_temp = values[1];
    var V_CAP_temp = values[2];
    var A_ENG_temp = values[3];
    var A_CAP_temp = values[4];
    var T_Air_in_temp = values[5];
    var T_Air_out_temp = values[6];
    var T_FC_H2O_out_temp = values[7];
    var Water_in_temp = values[8];
    var Water_out_temp = values[9];
    var Drive_SW_temp = values[12];
    var H2_flow_temp = values[23];
    var GPS_Speed_temp = values[27];
    var V_Safety_temp = values[28];
    var O2_calc_temp = values[30];


    var V_FC;
    var V_CAP;
    var A_ENG;
    var A_CAP;
    var T_Air_in;
    var T_Air_out;
    var T_FC_H2O_out;
    var Water_in;
    var Water_out;
    var Drive_SW;
    var H2_flow;
    var GPS_Speed;
    var V_Safety;
    var O2_calc;


    V_FC = parseFloat(V_FC_temp) * 0.001;
    V_CAP = parseFloat(V_CAP_temp) * 0.001;
    A_ENG = parseFloat(A_ENG_temp) * 0.001;
    A_CAP = parseFloat(A_CAP_temp) * 0.001;
    T_Air_in = parseFloat(T_Air_in_temp) * 0.1;
    T_Air_out = parseFloat(T_Air_out_temp) * 0.1;
    T_FC_H2O_out = parseFloat(T_FC_H2O_out_temp) * 0.1;
    Water_in = parseFloat(Water_in_temp) * 0.001;
    Water_out = parseFloat(Water_out_temp) * 0.001;
    Drive_SW = parseFloat(Drive_SW_temp) * 10;
    H2_flow = parseFloat(H2_flow_temp) * 0.01;
    GPS_Speed = parseFloat(GPS_Speed_temp) * 0.01;
    V_Safety = parseFloat(V_Safety_temp) * 0.001;
    O2_calc = parseFloat(O2_calc_temp) * 0.01;



    // update marker on map
     try {
        lat = values[31];
        lng = values[32];

        var latlng = L.latLng(parseFloat(lat), parseFloat(lng));
        //map.panTo(latlng);
        marker.setLatLng(latlng);
        marker.update();

	polyline.addLatLng(latlng);
	polyline.redraw();

    } catch (ex) {
        console.warn('Could not decode GPS position:', ex);

    }



    var now = new Date().getTime();
    //console.log(mma_x, mma_y);
    //console.log({ x: now, y: parseFloat(mma_x) });
    telemetry['V_FC'].push({ x: now, y: parseFloat(V_FC) });
    telemetry['V_CAP'].push({ x: now, y: parseFloat(V_CAP) });
    telemetry['A_ENG'].push({ x: now, y: parseFloat(A_ENG) });
    telemetry['A_CAP'].push({ x: now, y: parseFloat(A_CAP) });
    telemetry['T_Air_in'].push({ x: now, y: parseFloat(T_Air_in) });
    telemetry['T_Air_out'].push({ x: now, y: parseFloat(T_Air_out) });
    telemetry['T_FC_H2O_out'].push({ x: now, y: parseFloat(T_FC_H2O_out) });
    telemetry['Water_in'].push({ x: now, y: parseFloat(Water_in) });
    telemetry['Water_out'].push({ x: now, y: parseFloat(Water_out) });
    telemetry['Drive_SW'].push({ x: now, y: parseFloat(Drive_SW) });
    telemetry['H2_flow'].push({ x: now, y: parseFloat(H2_flow) });
    telemetry['GPS_Speed'].push({ x: now, y: parseFloat(GPS_Speed) });
    telemetry['V_Safety'].push({ x: now, y: parseFloat(V_Safety) });

    //console.log(telemetry['mma_x'].data);

    telemetry_graph['V_FC'].splice(0, telemetry_graph['V_FC'].length);
    telemetry['V_FC'].toArray().forEach(function(v) {telemetry_graph['V_FC'].push(v)}, this);

    telemetry_graph['V_CAP'].splice(0, telemetry_graph['V_CAP'].length);
    telemetry['V_CAP'].toArray().forEach(function(v) {telemetry_graph['V_CAP'].push(v)}, this);

    telemetry_graph['A_ENG'].splice(0, telemetry_graph['A_ENG'].length);
    telemetry['A_ENG'].toArray().forEach(function(v) {telemetry_graph['A_ENG'].push(v)}, this);
	
    telemetry_graph['A_CAP'].splice(0, telemetry_graph['A_CAP'].length);
    telemetry['A_CAP'].toArray().forEach(function(v) {telemetry_graph['A_CAP'].push(v)}, this);
	
    telemetry_graph['T_Air_in'].splice(0, telemetry_graph['T_Air_in'].length);
    telemetry['T_Air_in'].toArray().forEach(function(v) {telemetry_graph['T_Air_in'].push(v)}, this);
	
    telemetry_graph['T_Air_out'].splice(0, telemetry_graph['T_Air_out'].length);
    telemetry['T_Air_out'].toArray().forEach(function(v) {telemetry_graph['T_Air_out'].push(v)}, this);
	
    telemetry_graph['T_FC_H2O_out'].splice(0, telemetry_graph['T_FC_H2O_out'].length);
    telemetry['T_FC_H2O_out'].toArray().forEach(function(v) {telemetry_graph['T_FC_H2O_out'].push(v)}, this);
	
    telemetry_graph['Water_in'].splice(0, telemetry_graph['Water_in'].length);
    telemetry['Water_in'].toArray().forEach(function(v) {telemetry_graph['Water_in'].push(v)}, this);
	
    telemetry_graph['Water_out'].splice(0, telemetry_graph['Water_out'].length);
    telemetry['Water_out'].toArray().forEach(function(v) {telemetry_graph['Water_out'].push(v)}, this);
	
    telemetry_graph['Drive_SW'].splice(0, telemetry_graph['Drive_SW'].length);
    telemetry['Drive_SW'].toArray().forEach(function(v) {telemetry_graph['Drive_SW'].push(v)}, this);

    telemetry_graph['H2_flow'].splice(0, telemetry_graph['H2_flow'].length);
    telemetry['H2_flow'].toArray().forEach(function(v) {telemetry_graph['H2_flow'].push(v)}, this);
	
    telemetry_graph['GPS_Speed'].splice(0, telemetry_graph['GPS_Speed'].length);
    telemetry['GPS_Speed'].toArray().forEach(function(v) {telemetry_graph['GPS_Speed'].push(v)}, this);
	
    telemetry_graph['V_Safety'].splice(0, telemetry_graph['V_Safety'].length);
    telemetry['V_Safety'].toArray().forEach(function(v) {telemetry_graph['V_Safety'].push(v)}, this);

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
	
	$('#CenterMap').on('click', function() {
        map.panTo(new L.LatLng(parseFloat(lat), parseFloat(lng)));
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
