# Crossbar.io IoT Starterkit - Colorstrip

Seven [RGB neopixels](https://learn.adafruit.com/adafruit-neopixel-uberguide
) LED strip for high brightness and full color effects.

1. [Overview](#overview)
1. [How to run](#how-to-run)
1. [API](#api)

*Tags:* Python, GPIO, output, colorstrip

---

## Overview

This component exposes the seven RGB neopixel LED strip built into the Crossbar.io IoT Starterkit as a WAMP component which then can be used for visual indication and effects within a WAMP based application.

The seven RGB neopixel LED strip is connected via one of the PWM capable GPIOs of the Pi.

The component is written in Python using Autobahn running on Twisted. To program the LED strip, the component uses the [rpi_ws281x library](https://github.com/jgarff/rpi_ws281x).

The [Dockerfile](Dockerfile) for the component uses the default `crossbario/autobahn-python-armhf` image as base.


## How to run

Run the colorstrip component on the Pi following **[this procedure](https://github.com/crossbario/iotcookbook/tree/master/device/pi/components#how-to-run)**:

```console
cd iotcookbook/device/pi/component/colorstrip
make start
```

You should see a couple of visual patterns and animations on the neopixels, with the pixels remaining lit up at the end.

Then open this URL:

* [https://demo.crossbar.io/starterkit/colorstrip/web](https://demo.crossbar.io/starterkit/colorstrip/web)

in your browser.

The control page will ask you for the serial number of your Pi. This is being put out as part of the component startup logging, or you can do `grep Serial /proc/cpuinfo` and drop any leading zeros.

> Alternatively, you can construct the URL for direct access by adding '?serial=41f4b2fb' to its end, where you replace '41f4b2fb' with the serial of your Pi.

You should then see a Web page with some buttons for triggering light effects, and some input boxes and a button for setting the colorstrip to a color of your choosing.

This demonstrates secure remote procedure calls from any browser based device to an embedded device running a Python/Docker component and possibly behind firewalls and NATs.

> You can, of course, require authentication for the frontend in production.


## API

The component uses an URI prefix containing the Pi serial number

* `io.crossbar.demo.iotstarterkit.<serial>.colorstrip`

eg the Pi with serial no. `41f4b2fb` will use URIs starting with

* `io.crossbar.demo.iotstarterkit.41f4b2fb.colorstrip`


### Procedures

#### set_color

To set the color of a neopixel, call

* `io.crossbar.demo.iotstarterkit.<serial>.colorstrip.set_color(red, green, blue, k=null)`

with (positional) parameters

* `red`: Red component of color (`[0, 255]`)
* `green`: Green component of color (`[0, 255]`)
* `blue`: Blue component of color (`[0, 255]`)
* `k`: If given, set color of k-th pixel. Else set color of all pixels.

#### get_color

To get the current color of a neopixel, call

* `io.crossbar.demo.iotstarterkit.<serial>.colorstrip.get_color(k)`

with (positional) parameters

* `k`: Return color of k-th pixel.

#### flash

To shortly flash the neopixels is bright white, call

* `io.crossbar.demo.iotstarterkit.<serial>.colorstrip.flash(delay=50, repeat=5)`

with (positional) parameters

* `delay`: delay between flashes
* `repeat`: Number of flashes.


#### Effects

To play a whole effect, call one of the following

* `io.crossbar.demo.iotstarterkit.<serial>.colorstrip.lightshow()`
* `io.crossbar.demo.iotstarterkit.<serial>.colorstrip.color_wipe()`
* `io.crossbar.demo.iotstarterkit.<serial>.colorstrip.theater_chase()`
* `io.crossbar.demo.iotstarterkit.<serial>.colorstrip.rainbow()`
* `io.crossbar.demo.iotstarterkit.<serial>.colorstrip.rainbow_cycle()`
* `io.crossbar.demo.iotstarterkit.<serial>.colorstrip.theater_chaserainbow()`
* `io.crossbar.demo.iotstarterkit.<serial>.colorstrip.()`


### Events

#### on_color_set

The component will emit an event

* `io.crossbar.demo.iotstarterkit.<serial>.colorstrip.on_color_set(color)`

with `color` a dict with attributes:

* `led`: LED changed.
* `r`: R color component.
* `g`: G color component.
* `b`: B color component.
