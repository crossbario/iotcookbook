# Crossbar.io IoT Starterkit - Hex Display

Hex digit display, fully programmable as a WAMP component.

1. [Overview](#overview)
1. [How to run](#how-to-run)
1. [API](#api)

*Tags:* Python, I2C, LED, output, display

---

## Overview

This component exposes the six digit hex display built into the Crossbar.io IoT Starterkit as a WAMP component which then can be used to display information locally on the device. The display has high brightness LEDs and is daylight readable.

The Crossbar.io IoT Starterkit comes with a builtin six digit hexadecimal display that can be controlled from the Pi over I2C on address `0x77` (check via `sudo i2cdetect -y 1`). The display driver chip in the starterkit will drive the LED segments of the displays, while any pattern of LED on/off can be programmed from the software side.

The component is written in Python using Autobahn running on Twisted. The [Dockerfile](Dockerfile) for the component uses the default `crossbario/autobahn-python-armhf` image as base.


## How to run

Run the hex display component on the Pi following **[this procedure](https://github.com/crossbario/iotcookbook/tree/master/device/pi#how-to-run)**:

```console
cd iotcookbook/device/pi/component/buzzer
make start
```

Here is how that looks:

[![asciicast](https://asciinema.org/a/bhvvnuwo609gbn5b0l567pn78.png)](https://asciinema.org/a/bhvvnuwo609gbn5b0l567pn78)

Then open this URL:

* [https://demo.crossbar.io/iotcookbook/device/pi/recipes/buzzer?serial=41f4b2fb](https://demo.crossbar.io/iotcookbook/device/pi/recipes/hexdisplay?serial=41f4b2fb)

in your browser.

> Replace `41f4b2fb` with the serial number of your Pi (`grep Serial /proc/cpuinfo`).

You should see a Web page which allows you to control the hexdisplay (change color, start disco mode).

This demonstrates secure remote procedure calls from any browser based device to an embedded device running a Python/Docker component and possibly behind firewalls and NATs.

> The buttons ("caller") and buzzers ("callees") of course can be required to be authenticated as well as authorized in production.


## API

The component uses an URI prefix containing the Pi serial number

* `io.crossbar.demo.iotstarterkit.<serial>.buzzer`

eg the Pi with serial no. `41f4b2fb` will use URIs starting with

* `io.crossbar.demo.iotstarterkit.41f4b2fb.buzzer`


### Procedures

#### beep

To trigger a beeping sound sequence, call

* `io.crossbar.demo.iotstarterkit.<serial>.buzzer.beep(count, on, off)`

with (positional) parameters

* `count`: Number of beeps, default `1`.
* `on`: ON duration in ms, default `30`.
* `off`: OFF duration in ms, default `80`.

#### is_beeping

To check whether the buzzer is currently beeping, call

* `io.crossbar.demo.iotstarterkit.<serial>.buzzer.is_beeping()`

The procedure takes no parameters and returns a single positional result with a boolean flag.

#### welcome

To play a whole welcome beeping sequence, call

* `io.crossbar.demo.iotstarterkit.<serial>.buzzer.welcome()`

The procedure takes no parameters.


### Events

#### on_beep_started

The component will emit an event

* `io.crossbar.demo.iotstarterkit.<serial>.buzzer.on_beep_started(..)`

with keyword-based parameters:

* `count`: Number of beeps in the started sequence.
* `on`: ON duration in ms in the started sequence.
* `off`: OFF duration in ms in the started sequence.

#### on_beep_ended

When the current beeping sequence is finished, the component will emit en event

* `io.crossbar.demo.iotstarterkit.<serial>.buzzer.on_beep_ended()`


### Errors

When a beeping sequence is currently playing, calling `beep()` will raise an error:

* `io.crossbar.demo.iotstarterkit.<serial>.buzzer.already-beeping()`
