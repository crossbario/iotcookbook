console.log("Running on AutobahnJS ", autobahn.version);

// UI elements
var button = document.getElementById('button');
var status_url = document.getElementById('status_url');
var status_realm = document.getElementById('status_realm');
var status_serial = document.getElementById('status_serial');
var status_started = document.getElementById('status_started');

// get serial from document URL
var serial = document.location.search.split("=")[1];

if (!serial) {

   // show the serial input controls
   document.getElementById("serial").classList.remove("hidden");

} else {
   connect();
}

// the URI prefix the button component on the Pi is using
var prefix = 'io.crossbar.demo.iotstarterkit.' + serial + '.button.';

// the WAMP session
var session;

var prefix;

function connect() {

   // the URL of the WAMP Router (Crossbar.io)
   var wsuri;
   if (document.location.origin == "null" || document.location.origin == "file://") {
       wsuri = "wss://demo.crossbar.io/ws";
   } else {
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

       function on_beep_started (args, kwargs) {
           console.log('button pressed:', kwargs);
           notifier.style.backgroundColor = '#ff0';
       }

       function on_beep_ended () {
           console.log('button_released');
           notifier.style.backgroundColor = '#333';
       }
       function LED_on() {
          LED.style.backgroundColor = '#E8B32D';
       }

       function LED_off(){
        LED.style.backgroundColor = '#FFFFFF';
      }

      session.subscribe(prefix + 'button_pressed', on_beep_started);
      session.subscribe(prefix + 'button_released', on_beep_ended);
      session.subscribe(prefix + 'LED_off', LED_off);
      session.subscribe(prefix + 'LED_on', LED_on);
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
}

function serialEntered() {
   serial = document.getElementById("serialNumber").value;

   // --> same serial used on page reload
   window.location.replace(window.location.pathname + '?serial=' + serial);

   // --> enter new serial on reload (with other solutions this requires
   // editing the URL, which is cumbersome on mobile)
   // connect();
}


// this will be used from UI elements

function press() {
    if (session) {
        session.call(prefix + 'press',[]).then(
            function () {
                console.log('Website button pressed!');
            },
            function (err) {
                console.log('beeping failed:', err);
            }
        );
    } else {
        console.log('cannot beep: not connected');
    }
}


function led_on() {
    if (session) {
        session.call(prefix + 'led_on',[]).then(
            function () {
                console.log('Led activated');
            },
            function (err) {
                console.log('beeping failed:', err);
            }
        );
    } else {
        console.log('cannot beep: not connected');
    }
}


function led_off() {
    if (session) {
        session.call(prefix + 'led_off',[]).then(
            function () {
                console.log('LED deactivated');
            },
            function (err) {
                console.log('beeping failed:', err);
            }
        );
    } else {
        console.log('cannot beep: not connected');
    }
}
