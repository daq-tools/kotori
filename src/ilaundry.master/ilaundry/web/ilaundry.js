// -*- coding: utf-8 -*-
/*
 (c) 2014 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
 derived from https://github.com/tavendo/AutobahnPython/blob/master/examples/twisted/wamp/pubsub/simple/example2/index.html
 */

// WAMP session object
var sess;
var wsuri;

window.onload = function() {

    if (window.location.protocol === "file:") {
        wsuri = "ws://localhost:9000";
    } else {
        wsuri = "ws://" + window.location.hostname + ":9000";
    }

    // connect to WAMP server
    ab.connect(wsuri,

        // WAMP session was established
        function (session) {

            sess = session;
            console.log("Connected!");

            sess.prefix("broadcast", "http://ilaundry.useeds.de/broadcast#");
            //sess.prefix("node", "http://ilaundry.useeds.de/node/");
            sess.subscribe("broadcast:node-heartbeat", node_heartbeat);
            sess.prefix("washer-1", "http://ilaundry.useeds.de/node/washer-1#");
            sess.subscribe("washer-1:say", dump_event);
        },

        // WAMP session is gone
        function (code, reason) {

            sess = null;
            //alert(reason);
        }
    );
};

function dump_event(topic, event) {
    console.log({'topic': topic, 'event': event});
}

function node_heartbeat(topic, node_id) {
    console.log({'topic': topic, 'node_id': node_id});
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
    sess.publish(event_topic, message);
}
