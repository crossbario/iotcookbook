# Crossbar.io IoT Starterkit - Buzzer

This component exposes the piezo buzzer built into the Crossbar.io IoT Starterkit in a WAMP component.


## Hardware

The Crossbar.io IoT Starterkit has a built in piezo buzzer connected to GPIO 16 (Pin 36), with active high.

## Software

The component is written in Python using Autobahn running on Twisted.


## API

The component uses a URI prefix containing the Pi serial number. To check the serial number of your Pi:

```console
pi@raspberrypi:~/iotcookbook/device/pi/recipes/buzzer $ grep Serial /proc/cpuinfo
Serial      : 0000000041f4b2fb
```
Here, `41f4b2fb` is the serial number of the Pi inside the starterkit and the URI prefix will be

```
io.crossbar.demo.iotstarterkit.<41f4b2fb>.buzzer
```

### Procedures

To trigger a beeping sound sequence:

* `io.crossbar.demo.iotstarterkit.<serial>.buzzer.beep(count, on, off)`

with (positional) parameters

* `count`: Number of beeps, default `1`.
* `on`: ON duration in ms, default `30`.
* `off`: OFF duration in ms, default `80`.

To check whether the buzzer is currently beeping:

* `io.crossbar.demo.iotstarterkit.<serial>.buzzer.is_beeping()`

To play a whole welcome beeping sequence:

* `io.crossbar.demo.iotstarterkit.<serial>.buzzer.welcome()`


### Events

The component will emit an event

* `io.crossbar.demo.iotstarterkit.<serial>.buzzer.on_beep_started(..)`

with keyword-based parameters:

* `count`: Number of beeps in the started sequence.
* `on`: ON duration in ms in the started sequence.
* `off`: OFF duration in ms in the started sequence.

When the current beeping sequence is finished, the component will emit en event

* `io.crossbar.demo.iotstarterkit.<serial>.buzzer.on_beep_ended()`


### Errors

When a beeping sequence is currently playing, calling `beep()` will raise an error:

* `io.crossbar.demo.iotstarterkit.<serial>.buzzer.already-beeping()`
