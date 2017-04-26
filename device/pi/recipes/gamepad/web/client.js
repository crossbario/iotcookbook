console.log("Running on AutobahnJS ", autobahn.version);

// UI elements
var pad1 = document.getElementById('pad1');
var pad2 = document.getElementById('pad2');

var zini1 = document.getElementById('zini1');
var zini2 = document.getElementById('zini2');

var status_url = document.getElementById('status_url');
var status_realm = document.getElementById('status_realm');
var status_serial = document.getElementById('status_serial');
var status_started = document.getElementById('status_started');

// get serial from document URL
// .../iotcookbook/device/pi/recipes/gamepad/web/index.html?serial=41f4b2fb
var params = new URLSearchParams(document.location.search);
var serial = params.get('serial');
if (!serial) {
    var new_serial = prompt("Please enter serial No. of your Pi, eg 41f4b2fb");
    window.location.replace(window.location.pathname + '?serial=' + new_serial);
}

// the URI prefix the gamepad component on the Pi is using
var prefix = 'io.crossbar.demo.iotstarterkit.' + serial + '.gamepad.';

// the WAMP session
var session;

// the URL of the WAMP Router (Crossbar.io)
var wsuri;
if (document.location.origin == "null" || document.location.origin == "file://") {
    wsuri = "wss://demo.crossbar.io/ws";
} else {
    wsuri = (document.location.protocol === "http:" ? "ws:" : "wss:") + "//" + document.location.host + "/ws";
}

// the WAMP realm we join
var realm = "crossbardemo";

// the WAMP connection to the Router
var connection = new autobahn.Connection({
    url: wsuri,
    realm: realm
});


// fired when connection is established and session attached
connection.onopen = function (new_session, details) {
    console.log("Connected: ", details);
    session = new_session;

    status_realm.innerHTML = '' + details.authid + '@' + details.realm;
    status_url.innerHTML = '' + details.transport.url + ' (' + details.transport.protocol + ')';

    session.call(prefix + 'started').then(
        function (started) {
            status_serial.innerHTML = serial;
            status_started.innerHTML = started;
        },
        function (err) {
            if (err.error === 'wamp.error.no_such_procedure') {
                window.location.replace(window.location.pathname);
            } else {
                console.log(err);
            }
        }
    );

    function on_data (args, kwargs, details) {
        var last = args[0];
        var changed = args[1];

        console.log('gamepad data received (retained=' + details.retained + '):', last, changed);

        if (last.LB === 1) {
            pad1.style.backgroundColor = '#ff0';
        } else {
            pad1.style.backgroundColor = '#999';
        }

        if (last.RB === 1) {
            pad2.style.backgroundColor = '#ff0';
        } else {
            pad2.style.backgroundColor = '#999';
        }

        if (last.X1 || last.Y1) {
            var w = window.innerWidth;
            var h = window.innerHeight;
            var r;
            if (h < w) {
                r = h;
            } else {
                r = w;
            }
            if (last.X1) {
                var x = Math.round(w/2 + r * (last.X1 / 60000));
                zini1.style.left = '' + x + 'px';
            }
            if (last.Y1) {
                var y = Math.round(h/2 - r * (last.Y1 / 60000));
                zini1.style.top = '' + y + 'px';
            }
        }

        if (last.X2 || last.Y2) {
            var w = window.innerWidth;
            var h = window.innerHeight;
            var r;
            if (h < w) {
                r = h;
            } else {
                r = w;
            }
            if (last.X2) {
                var x = Math.round(w/2 + r * (last.X2 / 60000));
                zini2.style.left = '' + x + 'px';
            }
            if (last.Y2) {
                var y = Math.round(h/2 - r * (last.Y2 / 60000));
                zini2.style.top = '' + y + 'px';
            }
        }
    }

    session.subscribe(prefix + 'on_data', on_data, {get_retained: true});
};


// fired when connection was lost (or could not be established)
connection.onclose = function (reason, details) {
    console.log("Connection lost: " + reason);
    session = null;
    status_realm.innerHTML = '-';
    status_url.innerHTML = '-';
}


// now actually open the connection
connection.open();
