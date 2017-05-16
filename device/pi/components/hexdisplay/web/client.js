console.log("Running on AutobahnJS ", autobahn.version);

// UI elements
var status_url = document.getElementById('status_url');
var status_realm = document.getElementById('status_realm');
var status_serial = document.getElementById('status_serial');
var status_started = document.getElementById('status_started');

// get serial from document URL
// .../iotcookbook/device/pi/recipes/colorstrip/web/index.html?serial=41f4b2fb
var params = new URLSearchParams(document.location.search);
var serial = params.get('serial');
if (!serial) {
    var new_serial = prompt("Please enter serial No. of your Pi, eg 41f4b2fb");
    window.location.replace(window.location.pathname + '?serial=' + new_serial);
}

// the URI prefix the buzzer component on the Pi is using
var prefix = 'io.crossbar.demo.iotstarterkit.' + serial + '.hexdisplay.';

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
    status_serial.innerHTML = serial;

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

// our functions for controlling the hexdisplay

function show_info() {
   session.call(prefix + "show_info").then(
      function(res) {
         console.log("calling 'show_info' successfull!");
      },
      function(err) {
         console.log("calling 'show_info' resulted in error:", err)
      }
   )
}

function show_logo(logo) {
   session.call(prefix + "show_logo", [logo]).then(
      function(res) {
         console.log("calling 'show_logo' successfull!");
      },
      function(err) {
         console.log("calling 'show_logo' resulted in error:", err)
      }
   )
}

function scroll_message(str) {
   session.call(prefix + "scroll_message", [str]).then(
      function(res) {
         console.log("calling 'scroll_message', str successfull!");
      },
      function(err) {
         console.log("calling 'scroll_message', str resulted in error:", err)
      }
   )
}

function set_clear() {
   session.call(prefix + "set_clear", [str]).then(
      function(res) {
         console.log("calling 'set_clear' successfull!");
      },
      function(err) {
         console.log("calling 'set_clear' resulted in error:", err)
      }
   )
}
