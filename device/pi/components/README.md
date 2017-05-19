# Components

These are ready-to-use single-purpose components, packaged in Docker containers.

The give access to specific Pi functionality or hardware connected to the Pi via WAMP.

In many cases (once there are more components), all you'll need to get started developing is spinning up a Crossbar.io router, the necessary components on one or more Pis, with your software development work limited to a backend component which coordinates between the Pi components.

> The components are implemented in Python, JavaScript or C++. Unless you want to change something about the component functionality the implementation language is not something that concerns you. The most frequent change, adjusting the component URLs to fit within your application, does not require any language-specific knowledge.

## General

* [gamepad](gamepad) - Use an Xbox game controller connected to a Pi as a powerful, cheap real-time controller.
* [launchpad](launchpad) - A Novation Launchpad provides lots of buttons for your applications!

## Starterkit-related

The components below were created for the [Crossbar.io IoT Starerkit](http://crossbario.com/lab/crossbar-iot-starterkit/), but should work with the same hardware connected to a plain Pi.

* [buzzer](buzzer) - Control a piezo buzzer.
* [neopixel](neopixel) - Control a strip of neopixel full-color LEDs.
* [hexdisplay](hexdisplay) - Control a hexadecimal display.

We plan on adding more components over time

Currently on our radar:

* nfctag - read from and write to a NFC tag reader
* speechsynth - text-to-speech
* sampleplayer - play samples stored on the Pi, upload new samples
* photocamera - get a photo from a standard Web cam
* adcconv
* canbus
* chromeapp (see [here](https://developer.chrome.com/apps/first_app))

## How to Work with this

1. [How to run](#how-to-run)
    1. [Install Docker](#install-docker)
    2. [Clone the Cookbook](#clone-the-cookbook)
    3. [Run a Recipe](#run-a-recipe)
2. [How it works](#how-it-works)
    1. [Creating an app component image](#creating-an-app-component-image)
    1. [Starting an app component image](#starting-an-app-component-image)
    1. [Device URIs](#device-uris)

### How to run a Component

Getting started with the Pi recipes is very easy and quick, as we provide Docker base images for everthing. All you need is a Linux for the Pi (e.g. stock Raspbian) and Docker installed.

> The following describes how to run the [Buzzer Recipe](components/buzzer) as an example. All other Autobahn Python and JavaScript recipes work similar. The Autobahn C++ recipes work different though, please see the respective cookbook sections.


#### Install Docker

As we are using Docker, you will need to have a Docker enabled Rasbian or Linux running.

Docker on Rasbian is fully supported, but needs to be installed.

Download [Raspbian Jessie Lite](https://downloads.raspberrypi.org/raspbian_lite_latest), unpack and write the image to a SD card:

```console
sudo dd if=~/2017-04-10-raspbian-jessie-lite.img of=/dev/sdb bs=1M oflag=sync
```

To enable SSH server (this is required since 2016/11), mount the image on your PC and add a single empty file `/boot/ssh`

```console
touch /media/oberstet/boot/ssh
sudo sync
```

> Replace `/media/oberstet` with the mount path of the SD card with the mounted Rasbian image.

Now SSH into the Pi (the default hostname and default password is `raspberry`):

```console
ssh pi@raspberry.local
```

Update the system

```console
sudo apt update
sudo apt dist-upgrade
```

and install Docker

```console
curl -sSL get.docker.com | sh
sudo systemctl enable docker
sudo usermod -aG docker pi
sudo reboot
```

Test Docker by starting a shell in a plain Linux (Alpine) container:

```console
docker run -it --rm armhf/alpine /bin/sh
```


#### Clone the Cookbook

To work with the cookbook (or your fork thereof), here are two options:

**Option 1**

Clone the [crossbario/iotcookbook](https://github.com/crossbario/iotcookbook) repository **on your Pi**:

```console
ssh pi@raspberrypi.local
git clone https://github.com/crossbario/iotcookbook.git
```

> You should replace `pi@raspberrypi.local` here and in all command down below with the `user@hostname` of your Pi.

The advantage of this method is: it is simple and just works. The disadvantage is that you now have to edit your files *on* the Pi using an editor like nano or vim, and also commit and push from there.

**Option 2**

Alternatively, you can clone the repo **on your notebook**, and then mount it on your Pi.

The advantage using this method is an easier development workflow, since you can (directly) edit files on your notebook using eg Sublime or Atom, commit and push from there and only use the remote shell session on your Pi to restart your changed code and such.

We have documentation for two methods for this which work on the Pi in the [Crossbar.io Programming Guide](http://crossbar.io/docs/Development-with-External-Devices). They're both quick (as long as you're on a \*nix machine) and it's worht doing since it will save you a lot of time and frustration during development.


#### Run a Recipe

Regardless of which approach you've followed, now remotely log into your Pi, change to the directory within the cookbook repo with a component such as `buzzer` and start the component:

```console
cd iotcookbook/device/pi/components/buzzer
make start
```

When you start the component the *first* time, the respective Docker image needs to be built (on the Pi), which takes some time:

[![asciicast](https://asciinema.org/a/cu3bwe1iop99efxjpxhui8v42.png)](https://asciinema.org/a/cu3bwe1iop99efxjpxhui8v42)

When you start or restart the component later, the image is already built, and startup is quick:

[![asciicast](https://asciinema.org/a/bhvvnuwo609gbn5b0l567pn78.png)](https://asciinema.org/a/bhvvnuwo609gbn5b0l567pn78)

You should see the component starting in a container and hear a welcome beeping sequence:

```console
pi@raspberrypi:~/iotcookbook/device/pi/components/buzzer $ make start
docker build -t cookbook-buzzer -f Dockerfile .
Sending build context to Docker daemon  9.216kB
Step 1/5 : FROM crossbario/autobahn-python-armhf
 ---> 1dce1970750c
Step 2/5 : RUN pip install pyopenssl service_identity RPi.GPIO
 ---> Using cache
 ---> 5e623d43ce99
Step 3/5 : RUN rm -rf /app/*
 ---> Using cache
 ---> 2d6c3d1f0831
Step 4/5 : COPY ./app /app
 ---> Using cache
 ---> 865b2e34bd9e
Step 5/5 : CMD python -u client.py
 ---> Using cache
 ---> 8a7f5d00b861
Successfully built 8a7f5d00b861
docker run -it --rm \
    --device /dev/ttyAMA0 \
    --device /dev/mem \
    --device /dev/gpiomem \
    --privileged \
    --net=host \
    -e CBURL='wss://demo.crossbar.io/ws' \
    -e CBREALM='crossbardemo' \
    cookbook-buzzer
2017-04-26T12:54:37+0000 Crossbar.io IoT Starterkit Serial No.: 1106555643
2017-04-26T12:54:37+0000 BuzzerComponent connected: SessionDetails(realm=<crossbardemo>, session=1410140973480360, authid=<A6J9-7TEY-4U7E-SUPQ-EQRK-KH6E>, authrole=<anonymous>, authmethod=anonymous, authprovider=static, authextra=None, resumed=None, resumable=None, resume_token=None)
2017-04-26T12:54:37+0000 BuzzerComponent ready!
```

That's it. You've successfully deployed and run an Autobahn based application component that exposes hardware on the Pi as a WAMP component. The wrapped hardware can now interact with any other WAMP component in your overall application or system.

> The component connects to our public Crossbar.io demo instance. This is for convenience when initially quickly testing things. For actual development as well as deployment, you need to use your own Crossbar.io router (which is not difficult to set up).


### How it works

The component is built as a Docker image which derives from one of our Autobahn base images. The Docker image for the app component is then started on the Pi.

#### Creating an app component image

The `make start` command will first build a Docker image named `cookbook-buzzer`:

```console
docker build -t cookbook-buzzer -f Dockerfile .
```

The [Dockerfile](components/buzzer/Dockerfile) derives a component specific Docker image from one of the [base Docker images](https://github.com/crossbario/crossbar-docker/blob/master/IMAGES.md) we provide for Autobahn based components:


```console
FROM crossbario/autobahn-python-armhf

# install component specific dependencies
RUN pip install pyopenssl service_identity RPi.GPIO

# copy the component into the image
RUN rm -rf /app/*
COPY ./app /app

# start the component by default
CMD ["python", "-u", "client.py"]
```

The Docker image derives of `crossbario/autobahn-python-armhf`, which is the default, latest image we provide for components based on Autobahn and Python.

Next, component specific software dependencies are installed, such as the Python `RPi.GPIO` package.

Finally, the example `/app/*` contents that comes with the base images is replaced with our buzzer application code, everything from the `app` folder on the build host, and the image is configured to start `client.py` by default using Python.


#### Starting an app component image

After the image is built, a new container from the built Docker image named `cookbook-buzzer` is started:

```console
start: build
    docker run -it --rm \
        --device /dev/ttyAMA0 \
        --device /dev/mem \
        --device /dev/gpiomem \
        --privileged \
        --net=host \
        -e CBURL='wss://demo.crossbar.io/ws' \
        -e CBREALM='crossbardemo' \
        cookbook-buzzer
```

A few things are worth noting here:

The Crossbar.io router URL and realm the component should connect to are provided using environment variables `CBURL` and `CBREALM`.

Further, a couple of extra permissions are given to the started container to allow our code access the hardware connected to the host the container is running on, namely the Pi.

Finally, we allow arbitrary networking (this is to simplify things here, for production you want to restrict that).


#### Device URIs

Finally, the component uses a device URI prefix containing the Pi serial number. To check the serial number of your Pi:

```console
pi@raspberrypi:~ $ grep Serial /proc/cpuinfo
Serial      : 0000000041f4b2fb
```

The serial number with the leading `0` digits removed is `41f4b2fb`. Hence, an instance of the application component running on *this* Pi will use URIs of the form:

* `io.crossbar.demo.iotstarterkit.<serial>.buzzer.<suffix>`

with `41f4b2fb` for `<serial>`, and suffix parts like `beep` for `<suffix>`.

That way, eg each procedure on each device can be addressed in a systematic way.
