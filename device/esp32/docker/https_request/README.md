# Crossbar.io IoT ESP32 HTTPS - Call Docker

## Overview
This example uses the ESP32 and FreeRTOS to remote call a procedure off the Crossbar demo instance using a HTTPS-call over WIFI
the whole project will be build and flashed with a docker container

for setup the docker container please see [here](https://github.com/hassfers/working/tree/master/ESP32/docker#build-docker-container)

for the readme of the HTTPS example see [here](https://github.com/hassfers/working/tree/master/ESP32/examples/https_request)

there are three environment variables needed for a successful connection
```console
export WIFI_SSID="YOUR WIFI SSID"
export WIFI_KEY="YOUR WIFI PASSPHRASE"
CROSSBAR_HTTP_BRIDGE=https://cbdemo-eu-central-1.crossbar.io:443
```
and there are two ways to do this:
1. [pass it over during build](https://github.com/hassfers/working/tree/master/ESP32/docker#configure-the-makefile)
2. make a persisent environment variable and just pass over the name (method used here)  see [here](https://github.com/hassfers/working/tree/master/ESP32/examples/http_request#set-environment-variables) and [here](https://github.com/hassfers/working/tree/master/ESP32/docker#configure-the-makefile)
