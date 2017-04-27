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

        console.log('game-pad data received (retained=' + details.retained + ', last=' + JSON.stringify(last) + ', changed=' + JSON.stringify(changed) + ')');

        if ('LB' in changed) {
            if (last.LB === 1) {
                pad1.style.backgroundColor = '#ff0';
                rand_light(3, 0);
            } else {
                pad1.style.backgroundColor = '#999';
            }
        }

        if ('RB' in changed) {
            if (last.RB === 1) {
                pad2.style.backgroundColor = '#ff0';
                rand_light(0, 3);
            } else {
                pad2.style.backgroundColor = '#999';
            }
        }

        if (changed.X) {
            if (last.X == 1) {
                beep(5, 100, 50);
            }
        }
        if (changed.Y) {
            if (last.Y == 1) {
                beep(3, 300, 200);
            }
        }

        if (changed.A) {
            if (last.A == 1) {
                console.log('A');
                launchpad_reset();
            } else {
                console.log('A?', last.A);
            }
        }
        if (changed.B) {
            if (last.B == 1) {
                console.log('B');
                light_single_test();
            } else {
                console.log('B?', last.B);
            }
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

// this will be used from UI elements
function beep(count, on, off) {
    if (session) {
        var uri = 'io.crossbar.demo.iotstarterkit.' + serial + '.buzzer.beep';
        session.call(uri, [count, on, off]).then(
            function () {
                console.log('beeped!');
            },
            function (err) {
                console.log('beeping failed:', err);
            }
        );
    } else {
        console.log('cannot beep: not connected');
    }
}

function launchpad_reset() {
    if (session) {
        var uri = 'io.crossbar.demo.iotstarterkit.' + serial + '.launchpad.reset';
        session.call(uri).then(
            function () {
                console.log('reset!');
            },
            function (err) {
                console.log('reset failed:', err);
            }
        );
    } else {
        console.log('cannot test: not connected');
    }
}

function light_single_test() {
    if (session) {
        var uri = 'io.crossbar.demo.iotstarterkit.' + serial + '.launchpad.light_single_test';
        session.call(uri).then(
            function () {
                console.log('tested!');
            },
            function (err) {
                console.log('testing failed:', err);
            }
        );
    } else {
        console.log('cannot test: not connected');
    }
}

function rand_light(red,green) {
    if (session) {
        var uri = 'io.crossbar.demo.iotstarterkit.' + serial + '.launchpad.light';
        var x = Math.round(Math.random() * 8);
        var y = Math.round(Math.random() * 8);
        session.call(uri, [x, y, red, green]).then(
            function () {
                console.log('light set!');
            },
            function (err) {
                console.log('setting light failed:', err);
            }
        );
    } else {
        console.log('cannot test: not connected');
    }
}
