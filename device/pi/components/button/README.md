# Crossbar.io IoT Starterkit - Button and LED

## Overview

This component wramps a Button and a LED connected to the Rasperry Pis GPIO-Pins. The Button can be used for input and the LED can show warnings or just notifies the user about a special programm state.

The component is written in Python using Autobahn|Python running on Twisted. The [Dockerfile](Dockerfile) for the component uses the default `crossbario/autobahn-python-armhf` image as base.


## How to run

Run the button component on the Pi following **[this procedure](https://github.com/crossbario/iotcookbook/tree/master/device/pi/components#how-to-run)**:

```console
cd iotcookbook/device/pi/component/button
make start
```


(and it may take a while on first start as the necessary Docker image is downloaded).

Then open this URL:

* [https://demo.crossbar.io/iotcookbook/device/pi/recipes/button](https://demo.crossbar.io/iotcookbook/device/pi/recipes/button)

in your browser.

The control page will ask you for the serial number of your Pi. This is being put out as part of the component startup logging, or you can do `grep Serial /proc/cpuinfo` and drop any leading zeros.

> Alternatively, you can construct the URL for direct access by adding '?serial=41f4b2fb' to its end, where you replace '41f4b2fb' with the serial of your Pi.

You should then see a Web page with buttons to control the LED connected to your Pi on GPIO PIN 15. Pressing the button connected to PIN 18 a button on the Web page will issue a WAMP remote procedure call to the `press()` procedure exposed by the button component running on the Pi. Additionally there is a small square which turns yellow for a second if the pressed procedure is called.

There is also a button which has the same function as if the button on the Raspberry is pressed. So you can test the communication between your raspberry and your browser.

This demonstrates secure remote procedure calls from any browser based device to an embedded device running a Python/Docker component and possibly behind firewalls and NATs.


## API

The component uses an URI prefix containing the Pi serial number

* `io.crossbar.demo.iotstarterkit.<serial>.button`

eg the Pi with serial no. `41f4b2fb` will use URIs starting with

* `io.crossbar.demo.iotstarterkit.41f4b2fb.button`


### Procedures

#### press

Trigger a procedure that you can make a virtual button press

* `io.crossbar.demo.iotstarterkit.<serial>.button.press`


#### led_on

Switches the LED on connected to the pi

* `io.crossbar.demo.iotstarterkit.<serial>.button.led_on`

#### led_off

Switches the LED off connected to the pi

* `io.crossbar.demo.iotstarterkit.<serial>.button.led_off`


### Events

#### button_pressed

The component will emit an event when the Button is pressed

* `io.crossbar.demo.iotstarterkit.<serial>.button.button_pressed()`


#### button_released

After one second the button_released event will be published

* `io.crossbar.demo.iotstarterkit.<serial>.button.button_released()`


### Errors

When between button_pressed and button_released event, the button is pressed again you will see this error

* `io.crossbar.demo.iotstarterkit.<serial>.button.is_pressed()`



