# Raspberry Pi - Gamepad

This component exposes a wireless Xbox controller connected to a Raspberry Pi as a WAMP component.

The Xbox controller is wrapped as a WAMP component and can then be used as a powerful real-time input controller within a WAMP based application.


## How to run

First, add the following to `/boot/cmdline.txt`

```
dwc_otg.fiq_fsm_mask=0x7
```

and reboot the Pi.

> The need for this is explained [here](https://discourse.osmc.tv/t/april-update-xboxdrv-not-working/15291/26) and [here](https://www.raspberrypi.org/forums/viewtopic.php?t=70437).

Run the gamepad component on the Pi following [this](https://github.com/crossbario/iotcookbook/tree/master/device/pi#how-to-run) general procedure.

[![asciicast](https://asciinema.org/a/edyrral22af5z86ey77i8k3lh.png)](https://asciinema.org/a/edyrral22af5z86ey77i8k3lh)

Then open

* [https://demo.crossbar.io/iotcookbook/device/pi/recipes/gamepad?serial=41f4b2fb](https://demo.crossbar.io/iotcookbook/device/pi/recipes/gamepad?serial=41f4b2fb)

in your browser - anywhere.

> Replace `41f4b2fb` with the serial No. of your Pi (`grep Serial /proc/cpuinfo`).

You should see a Web frontend that shows two buttons and two anlog controls of the Xbox controller in real-time.


## Hardware

You will need a Microsoft Xbox controller, a wired one or a wireless one with a USB receiver connected via USB to your Raspberry Pi.


## Software

The component is written in Python using Autobahn running on Twisted.

The [Dockerfile](Dockerfile) for the component uses the default `crossbario/autobahn-python-armhf` image as base.

Further, the component uses [xboxdrv](https://github.com/xboxdrv/xboxdrv), a Xbox gamepad userspace driver for Linux. The Python component talks to xboxdrv over stdin pipe. xboxdrv when running will output gamepad controller values by printing lines to stdout, and the Python component receives these lines via stdin, parses the lines, and publishes WAMP events.


## API

The component uses an URI prefix containing the Pi serial number

* `io.crossbar.demo.iotstarterkit.<serial>.gamepad`

eg the Pi with serial no. `41f4b2fb` will use URIs starting with

* `io.crossbar.demo.iotstarterkit.41f4b2fb.gamepad`


### Procedures

#### started

To get the UTC timestamp (ISO8601 format) when the component started, call

* `io.crossbar.demo.iotstarterkit.<serial>.gamepad.started()`

The procedure takes no parameters and returns the timestamp as a string.

#### get_data

To retrieve the latest full set of gamepad readings, call

* `io.crossbar.demo.iotstarterkit.<serial>.gamepad.get_data()`

The procedure takes no parameters and returns a single positional result with a dictionary:

* A
* B
* LB
* LT
* RB
* TL
* TR
* X
* X1
* X2
* Y
* Y1
* Y2
* back
* dd
* dl
* dr
* du
* guide
* start

### Events

#### on_data

The component will emit an event

* `io.crossbar.demo.iotstarterkit.<serial>.gamepad.on_data(last, changed)`

with two positional parameters:

* `last`: The latest full set of readings from the gamepad.
* `changed`: The changed readings in this event compared to the latest state before

Both attributes are dictionaries with attributes as listed in `get_data()`.
