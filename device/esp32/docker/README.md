# Docker for ESP32

this library contains examples for working with an ESP32 and uses the IDE and the toolchain in a docker container.

## What you need
- a ESP-chip
- [docker installed on your pc](https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/)

## Build docker container

First thing you have to build the docker container.
Clone the docker-file in a folder of your choice
Run:
```console
 make build
```
it will take a while depend on your download speed and build a docker container named "esp32"

## Build and flash your project

There are different ways to use the makefile:

```console
make esp32
```
will just build your project into a folder named "build"

```console
make esp32_monitor
```
will start the debugging serial monitor for your ESP32 only

```console
make esp32_flash
```
will only build and flash your program to your ESP32

```console
make esp32_all
```
will build and flash your program and start the debug monitor after flashing


```console
make esp32_bash
```

this will start an interactive bash environment in your docker container. this is a great thing for development cause you only have to build the whole library once you open the container.
Next time it will only compile the changes you made.

## Configure the Makefile

of course its possible two adapt the make file for your project and there are several things you need to know:

If you want to set environment variables you have to put an ```-e``` in Front of your variable name like:
```console
-e WIFI_KEY
```
if its a known variable or
```console
-e WIFI_KEY ="foo"
```
if its a new one

if you want to avoid to be asked your project settings you have to set the make variable ```BATCH_BUILD=1```
now the IDE will set all the settings to the default values and most of the times the build will be successful
If there are special settings needed there will be a error prompt and you have to run
```console
 make esp32_bash
 make menuconfig
```
