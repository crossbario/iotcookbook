# Crossbar.io IoT ESP32 HTTPS - Call

## Overview
This example uses the ESP32 and FreeRTOS to remote call a procedure off the Crossbar demo instance using a HTTPS-call over WIFI

## Important
The ESP32 embedded TLS library doesn't contain any CA or Root certificates.
You have to load the full CA-Chain you need into your program.
In this example there are two needed.
- [ISRGROOTX1](https://letsencrypt.org/certs/isrgrootx1.pem.txt) and
- [Letsencryptauthorityx3](https://letsencrypt.org/certs/letsencryptauthorityx3.pem.txt)

if these are outdated you can find fresh ones [here](https://letsencrypt.org/certificates/)

after downloading the certificates you have to put them in one file in the given order.


## What you need
- a ESP-chip
- the  ESP-SKD (how to install following the instructions found [here](https://esp-idf.readthedocs.io/en/v1.0/))



## How to run
### Set environment variables
The first thing you have to do is set a few environment variables needed for WIFI connection
so type in your terminal window
```console
export WIFI_SSID="YOUR WIFI SSID"
export WIFI_KEY="YOUR WIFI PASSPHRASE"
CROSSBAR_HTTP_BRIDGE=https://cbdemo-eu-central-1.crossbar.io:443
```
>alternatively you can set these variables in your ~/.profile file so you don't have to repeat this step every time you restart your bash
>
the value ```CROSSBAR_HTTP_BRIDGE``` will be parsed to protocol, host and port.
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
I (372) example: Seeding the random number generator
I (382) example: Loading the CA root certificate...
I (392) example: Setting hostname for TLS session...
I (392) example: Setting up the SSL/TLS structure...
I (2222) example: Connected to AP
I (2222) example: Connecting to cbdemo-eu-central-1.crossbar.io:443...
I (2282) example: Connected.
I (2282) example: Performing the SSL/TLS handshake...
I (4642) example: Verifying peer X.509 certificate...
I (4652) example: Certificate verified.
I (4652) example: Writing HTTP request..
```
The important lines are the four above. If they look like this you have successful connected to the Crossbar  Demo Instance over TLS and the communication is encrypted.
```console
REQUEST: POST /call HTTP/1.0
Host: cbdemo-eu-central-1.crossbar.io
User-Agent: esp-idf/1.0 esp32
Accept: */*
Content-Type: application/json
Content-Length: 65

{"procedure":"com.example.split_name","args":["Maxi Mustermann"]}
```
this is a complete print of the sended HTTP-Package. You can separate it in two parts:
- Header    (where all the connection informations are in)
- Payload   (the content you want to send. Here you have to put in which function of the Crossbar instance               you want to call and what the parameters should be)

 In this example the same HTTP-Package is sended as in the HTTP example, but this time its sended over TSL, to the crossbar demo instance. This instance has no procedure called "com.example.split_name" and so we get the following output.

```console
HTTP/1.0 200 OK
Server: Crossbar/17.5.1
Date: Mon, 31 Jul 2017 13:48:33 GMT
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
Cache-Control: no-store,no-cache,must-revalidate,max-age=0
Content-Type: application/json; charset=UTF-8

{"error": "wamp.error.no_such_procedure", "args": ["no callee registered for procedure <com.example.split_name>"], "kwargs": {}}
```
If you get this answer, you know that everything with your connection works well and you only have to implement the wanted procedure at your crossbar instance.




