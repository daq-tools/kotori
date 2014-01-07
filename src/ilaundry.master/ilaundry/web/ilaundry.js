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
            sess.subscribe("broadcast:node-activity", dump_event);
            sess.subscribe("broadcast:node-activity", node_activity);
            sess.subscribe("broadcast:node-privacy", dump_event);
            sess.subscribe("dashboard:update", dashboard_update);

            // trigger dashboard update
            sess.publish("dashboard:update", null, false);

        },

        // WAMP session is gone
        function(code, reason) {
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

function node_activity(topic, event) {
    var node_id = event.node_id;
    var state = event.state;
    console.log({'topic': topic, 'node_id': node_id, 'state': state});
}

function dashboard_update(topic, event) {
    sess.call("registry:get_nodelist").then(function(nodelist) {
        ab.log('nodelist: ' + nodelist);
        var node_select = document.getElementById("node_id");
        node_select.options.length = 0;
        for (index in nodelist) {
            var node_id = nodelist[index];
            node_select.options[node_select.options.length] = new Option(node_id, node_id);
        }
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
    sess.publish(event_topic, message);
}
