var session = null;
      var image = document.getElementById("image");
      var imageProgress = document.getElementById("imageProgress");

      // the URL of the WAMP Router (Crossbar.io)
      var wsuri;
      if (document.location.origin == "file://") {
         wsuri = "wss://demo.crossbar.io/ws"; // localhost for development
      } else {
         wsuri = (document.location.protocol === "http:" ? "ws:" : "wss:") + "//" +
                     document.location.host + "/ws"; // URL of the Crossbar.io instance this is served from
      }



      // the WAMP connection to the Router
      //
      var connection = new autobahn.Connection({
         url: wsuri, // replace with URL of WAMP router if this doesn't serve the file
         realm: "crossbardemo"
      });

      var cameraResult = null;

      var requestPhoto = function () {

         session.call("io.crossbar.demo.iotstarterkit.6afe83b4.camera.take_photo").then(
            function (res) {
                console.log("image received", res);

               imageProgress.innerHTML = "";

               base64image = res[1];
               // need to remove the header and footer which uuencode adds
               base64image = base64image.slice(29);
               base64image = base64image.slice(0, -6);

               image.src = "data:image/jpg;base64," + base64image;

            },
            function (err) {
               console.log("requestImage failed", err);
               imageProgress.innerHTML = "Error getting image!";
            }
         );
      };

      // fired when connection is established and session attached
      //
      connection.onopen = function (sess, details) {

         session = sess;

         console.log("connected");

         document.getElementById("shutter").addEventListener("click", requestPhoto);

         status_realm.innerHTML = '' + details.authid + '@' + details.realm;
         status_url.innerHTML = '' + details.transport.url + ' (' + details.transport.protocol + ')';



      };

      // fired when connection was lost (or could not be established)
      //
      connection.onclose = function (reason, details) {

         console.log("Connection lost: " + reason);

         session = null;
         status_realm.innerHTML = '-';
         status_url.innerHTML = '-';

      }

      // now actually open the connection
      //
    //   connection.open();


    // get serial from document URL
    var serial = document.location.search.split("=")[1];

    if (!serial) {

       // show the serial input controls
       document.getElementById("serial").classList.remove("hidden");

    } else {
       connection.open();
    }

    function serialEntered() {
       serial = document.getElementById("serialNumber").value;

       // --> same serial used on page reload
       window.location.replace(window.location.pathname + '?serial=' + serial);

    }
