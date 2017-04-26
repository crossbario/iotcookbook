# Crossbar.io IoT Starterkit - Buzzer

This component exposes the piezo buzzer built into the Crossbar.io IoT Starterkit in a WAMP component. The piezo buzzer is wrapped as a WAMP component and can then be used as a acoustic warning or notification device within a WAMP based application.


## How to run

Run the buzzer component on the Pi following [this](https://github.com/crossbario/iotcookbook/tree/master/device/pi#how-to-run) general procedure.

Then open

    https://demo.crossbar.io/iotcookbook/device/pi/recipes/buzzer?serial=41f4b2fb

in your browser - anywhere.

> Replace `41f4b2fb` with the serial No. of your Pi (`grep Serial /proc/cpuinfo`).

You should see a Web frontend that allows you to control the piezo buzzer on the Pi remotely.


## Hardware

The Crossbar.io IoT Starterkit has a built in piezo buzzer connected to GPIO 16 (Pin 36) with active high.


## Software

The component is written in Python using Autobahn running on Twisted. The [Dockerfile](Dockerfile) for the component uses the default `crossbario/autobahn-python-armhf` image as base.


## API

The component uses a URI prefix containing the Pi serial number. To check the serial number of your Pi:

```console
pi@raspberrypi:~ $ grep Serial /proc/cpuinfo
Serial      : 0000000041f4b2fb
```
Here, `41f4b2fb` is the serial number of the Pi inside the Starterkit and the URI prefix used will be

```
io.crossbar.demo.iotstarterkit.<41f4b2fb>.buzzer
```

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
