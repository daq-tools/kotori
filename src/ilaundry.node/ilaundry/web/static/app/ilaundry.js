// -*- coding: utf-8 -*-
/*
 (c) 2014 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
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

// Grab the HTML out of our template tag and pre-compile it.
var node_template = _.template(
    $("#node-template").html()
);

// WAMP session object
var sess;
var nodes = {};

window.onload = function() {

    // websocket url defaults
    if (!wsuri) {
        if (window.location.protocol === "file:") {
            wsuri = "ws://localhost:9000";

        } else {
            wsuri = "ws://" + window.location.hostname + ":9000";
        }
    }

    // explicitly specified websocket url
    var url = $.url(window.location.href);
    var master_uri = url.param('master');
    if (master_uri) wsuri = master_uri;

    console.log('[WAMP] INFO: Connecting to ' + wsuri);

    //ab.debug(true, true, true);

    // connect to WAMP server
    ab.connect(wsuri,

        // WAMP session was established
        function(session) {

            sess = session;
            console.log("Connected!");

            sess.prefix("registry", "http://ilaundry.useeds.de/registry#");
            sess.prefix("broadcast", "http://ilaundry.useeds.de/broadcast#");
            sess.prefix("dashboard", "http://ilaundry.useeds.de/dashboard#");

            sess.subscribe("broadcast:node-heartbeat", node_heartbeat);
            //sess.subscribe("broadcast:node-activity", dump_event);
            sess.subscribe("broadcast:node-activity", node_state);
            sess.subscribe("broadcast:node-privacy", node_state);
            sess.subscribe("dashboard:update", dashboard_update);

            // trigger dashboard update
            sess.publish("dashboard:update", null, false);

        },

        // WAMP session is gone
        function(code, reason) {
            console.log('[WAMP] ERROR: ' + 'code: ' + code + ', reason: ' + reason);
            sess = null;
            //alert(reason);
            dashboard_clear();
        }
    );
};

function dump_event(topic, event) {
    console.log({'topic': topic, 'event': event});
}

function node_heartbeat(topic, node_id) {
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

    sess.call("registry:get_nodelist").then(function(nodelist) {
        ab.log('nodelist: ' + nodelist);

        //dashboard_clear();

        for (index in nodelist) {
            var node_id = nodelist[index];
            if (node_id in nodes) {
                continue;
            }
            nodes[node_id] = true;

            var template_data = {node_id: node_id};
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

        }

        // indicate node online/offline state
        $.each(nodes, function(node_id, state) {
            console.log(node_id);
            if ($.inArray(node_id, nodelist) != -1) {
                node_online(node_id);
            } else {
                nodes[node_id] = false;
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
        console.error('ERROR: No WAMP session with iLaundry master service');
        return;
    }

    var node_topic = 'http://ilaundry.useeds.de/node/' + node_id + '#';
    sess.prefix(node_id, node_topic);
    //sess.subscribe(node_topic, dump_event);
    var event_topic = node_id + ':say';
    console.log('publishing: ' + event_topic + ' ' + message)
    sess.publish(event_topic, message);
}
