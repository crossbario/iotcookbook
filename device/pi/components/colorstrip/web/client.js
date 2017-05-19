console.log("Running on AutobahnJS ", autobahn.version);

// UI elements
var status_url = document.getElementById('status_url');
var status_realm = document.getElementById('status_realm');
var status_serial = document.getElementById('status_serial');
var status_started = document.getElementById('status_started');

// get serial from document URL

// nice, but not supported on IE11 or Edge (2017-05)
// var params = new URLSearchParams(document.location.search);
// var serial = params.get('serial');

var serial = document.location.search.split("=")[1];

if (!serial) {

   // show the serial input controls
   document.getElementById("serial").classList.remove("hidden");

} else {
   connect();
}

// the WAMP session
var session;

var prefix;

function connect() {

   // the URI prefix the buzzer component on the Pi is using
   prefix = 'io.crossbar.demo.iotstarterkit.' + serial + '.colorstrip.';
   console.log("prefix", prefix);


   // the URL of the WAMP Router (Crossbar.io)
   var wsuri;
   if (document.location.origin == "null" || document.location.origin == "file://") {
       wsuri = "wss://demo.crossbar.io/ws";
   } else {
      // works when file served by the static file server in Crossbar.io
      // with a Web transport configured for both the file serving and
      // WebSocket connections
       wsuri = (document.location.protocol === "http:" ? "ws:" : "wss:") + "//" + document.location.host + "/ws";
   }

   // For testing only
   wsuri = "wss://demo.crossbar.io/ws";

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

       // enable the controls
       document.getElementById('control').classList.remove('inactive');

   };

   // fired when connection was lost (or could not be established)
   connection.onclose = function (reason, details) {
      console.log("Connection lost: " + reason);
      session = null;
      status_realm.innerHTML = '-';
      status_url.innerHTML = '-';

      // disable the controls
      document.getElementById('control').classList.add('inactive');
   }

   // now actually open the connection
   connection.open();

}

function serialEntered() {
   serial = document.getElementById("serialNumber").value;

   // --> same serial used on page reload
   window.location.replace(window.location.pathname + '?serial=' + serial);

   // --> enter new searial on reload (with other solutions this requires
   // editing the URL, which is cumbersome on mobile)
   // connect();
}

// our functions for controlling the colorstrip

function trigger(whichShow) {
   console.log("prefix in whichShow", prefix);
   session.call(prefix + whichShow).then(
      function(res) {
         console.log("calling " + whichShow + " successfull!");
      },
      function(err) {
         console.log("calling " + whichShow  + " resulted in error:", err)
      }
   )
}

function setColor() {
   var red = parseInt(document.getElementById("red").value);
   var green = parseInt(document.getElementById("green").value);
   var blue = parseInt(document.getElementById("blue").value);

   session.call(prefix + "set_color", [red, green, blue]).then(
      function(res) {
         console.log("calling 'set_color' succeeded");
      },
      function(err) {
         console.log("calling 'set_color' resulted in error:", err)
      }
   )
}
