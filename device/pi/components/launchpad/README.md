# Crossbar.io IoT Starterkit - Launchpad

Use a Novation Launchpad as an input with lots of buttons.

1. [Overview](#overview)
2. [How to run](#how-to-run)
3. [API](#api)

*Tags:* Python, input, launchpad

---

## Overview

This component exposes a Novation Launchpad connected to the Pi via USB as a multi-button controller.

The component is written in Python using Autobahn|Python running on Twisted. The [Dockerfile](Dockerfile) for the component uses the default `crossbario/autobahn-python-armhf` image as base.

## How to run

Run the buzzer component on the Pi following **[this procedure](https://github.com/crossbario/iotcookbook/tree/master/device/pi/components#how-to-run)**:

```console
cd iotcookbook/device/pi/component/buzzer
make start
```




## API
