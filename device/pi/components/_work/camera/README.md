# Raspberry Pi Camera component

> may be out of date

The Raspberry Pi Camera component allows the remote triggering of a photo via a WAMP procedure call. The photo is returned as the call result.

![Raspberry Pi with camera](/static/img/iotcookbook/camera_raspberry_pi.jpg)

## Trying it out

The code for this can be found in the [crossbarexamples GitHub repository](https://github.com/crossbario/crossbarexamples) under `iotcookbook`. You need to clone this (or [download it as a ZIP file](https://github.com/crossbario/crossbarexamples/archive/master.zip)).

The Pi should support most standard WebCams once you've done

    sudo apt-get install fswebcam

To try it whether this works, do

    fswebcam image.jpg

and then open the image.

Then open a shell for the component directory on your computer.

Start up Crossbar.io:

    crossbar start

This also serves a frontend which allows you to trigger the taking of an image and displays the progress feedback as well as the image `http://localhost:8080`.

In `camera_pi.js`, add the URL of the machine on which Crossbar.io runs:

```javascript
var connection = new autobahn.Connection({
    // replace with the url of your crossbar instance
    url: "ws://<URL OF YOUR CROSSBAR INSTANCE>/ws",
    realm: "iot_cookbook"
});
```

Then get `camera_pi.js` onto the Raspberry Pi, e.g. by doing

    scp camera_pi.js pi@<IP of your Pi>:~/

`camera_pi.js` is run using Node.js, so you need this installed, and additionally npm, Node.js's package managenment, and Autobahn|JS. Once you've got Node.js and npm, in the directory where `camera_pi.js`is, do

    npm install autobahn

(In case you get a certificate error, doing

    npm config set registry http://registry.npmjs.org/

is one way to solve this, though you now no longer use https!)

We also need `uuencode`, which we install by doing

    sudo apt-get install sharutils

Now run our camera component using Node.js

    nodejs camera_pi.js

This should log

```console
Raspberry Pi Camera starting
connected
Procedure 'io.crossbar.examples.pi.camera.take_photo' registered: 1902454329
...
```

Once this is running, in the browser frontend click on `take photo`. The default image of a burglar should be replaced with an image of whatever is in front of your webcam.

## The API

The component exposes a single procedure `io.crossbar.examples.pi.camera.take_photo`.

The result is a base64 encoded image. As a default this is JPG, but can be changed (in 'camera_pi.js', see the [fswebcam documentation](http://manpages.ubuntu.com/manpages/lucid/man1/fswebcam.1.html)). Due to the encoding using 'uuencode' on the Pi, header & footer need to be removed before this can be used in a data URI.

## Using it

In your own project:

* Adapt the procedure URL for taking a photo to your own needs.
