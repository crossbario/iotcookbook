# Crossbar.io IoT ESP32 HTTP - Call

## Overview
This example uses the ESP32 and FreeRTOS to remote call a procedure running on a Crossbar instance using a HTTP-call over WIFI

## What you need
- a ESP-chip
- the  ESP-SKD (how to install following the instructions found [here](https://esp-idf.readthedocs.io/en/v1.0/))
- a crossbar demo instance to answer your call ([look here](https://github.com/crossbario/crossbar-examples/tree/master/rest/caller))


## How to run
### Set environment variables
The first thing you have to do is set a few environment variables needed for WIFI connection
so type in your terminal window
```console
export WIFI_SSID="YOUR WIFI SSID"
export WIFI_KEY="YOUR WIFI PASSPHRASE"
export CROSSBAR_PORT=8080
export CROSSBAR_SERVER="THE IP ADDRESS OF YOUR CROSSBAR INSTANCE"
export CROSSBAR_URL=http://"THE IP ADDRESS OF YOUR CROSSBAR INSTANCE"/
```
>alternatively you can set these variables in your ~/.profile file so you dont have to repeat this step everytime you restart your bash
>

### Build the ESP example

after cloning the repo just jump in the downloaded folder and run

```console
make -j5
```
if your toolchain is installed right, it will build the whole project include the bootloader in a folder called "build"

after building successful run
```console
make flash monitor
```
this will download the project to your chip and run the serial monitor for debug output after finished flashing

### Run the Program
#### ESP32-Serial Monitor
on your serial monitor you can see, after heaps of bootloader output, something like:

```console
POST /call HTTP/1.0
Host: "YOUR CROSSBAR INSTANCE IP"
User-Agent: esp-idf/1.0 esp32
Accept: */*
Content-Type: application/json
Content-Length: 65

{"procedure":"com.example.split_name","args":["Maxi Mustermann"]}
```
this is a complete print of the sended HTTP-Package. You can separate it in two parts:
- Header    (where all the connection informations are in)
- Payload   (the content you want to send. Here you have to put in which function of the Crossbar instance you want to call and what the parameters should be)

if everything gone well there should be a other message showing something like

```console
HTTP/1.0 200 OK
Server: Crossbar/17.3.1
Date: Fri, 30 Jun 2017 09:37:07 GMT
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
Cache-Control: no-store,no-cache,must-revalidate,max-age=0
Content-Type: application/json; charset=UTF-8

{"args":["Maxi","Mustermann"]}
```
this is the answer from Crossbar

#### Crossbar-Console
You can also see a log message in your Crossbar Console Window showing that everything went well
```console
2017-06-30T11:51:18+0200 [Router      21170] split_name() called with 'Maxi Mustermann'
```




