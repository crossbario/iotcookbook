# Raspberry Pi and Crossbar.io IoT Starterkit Cookbook

This part of the IoT Cookbook provides information, howtos and [recipes](recipes) for the Raspberry Pi and the Crossbar.io IoT Starterkit.


## How to run

Running the recipes here is only few commands away, eg the following describes how to run the [Buzzer Recipe](recipes/buzzer).

This assumes you have a Linux with Docker running on the Pi, eg Raspbian with Docker.

First clone the [crossbario/iotcookbook](https://github.com/crossbario/iotcookbook) repository **on your Pi**:

```console
ssh pi@raspberrypi.local
git clone https://github.com/crossbario/iotcookbook.git
```

> You should replace `pi@raspberrypi.local` here and in all command down below with the `user@hostname` of your Pi.

Alternatively, you can clone the repo **on your notebook**:

```console
cd ~
git clone https://github.com/crossbario/iotcookbook.git
```

then create a mountpoint on the Pi
```console
ssh pi@raspberrypi.local mkdir -p iotcookbook
```

and then mount your local working copy *on* your Pi *from* your notebook:

```console
dpipe /usr/lib/openssh/sftp-server = ssh pi@raspberrypi.local \
    sshfs :${HOME}/iotcookbook /home/pi/iotcookbook -o slave &
```

The advantage using the latter method is an easier development workflow, since you can edit files on your notebook, and only use the remote shell session on your Pi to restart your changed code and such.

> Above command makes use of a technique called "reverse SSHFS", eg see [here](https://blog.dhampir.no/content/reverse-sshfs-mounts-fs-push)

Regardless of which approach you've followed, now remotely log into your Pi and start the component:

```
cd iotcookbook/device/pi/recipes/buzzer
make start
```

You should see the component starting in a container and hear a welcome beeping sequence:

```console
pi@raspberrypi:~/iotcookbook/device/pi/recipes/buzzer $ make start
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


The component uses a URI prefix containing the Pi serial number. To check the serial number of your Pi:

```console
pi@raspberrypi:~ $ grep Serial /proc/cpuinfo
Serial      : 0000000041f4b2fb
```


That's it. You've successfully deployed and run an Autobahn based application component that exposes hardware on the Pi as a WAMP component. The wrapped hardware can now interact with any other WAMP component in your overall application or system.


## How it works

The `make start` command will first build a Docker image named `cookbook-buzzer`:

```console
docker build -t cookbook-buzzer -f Dockerfile .
```

The [Dockerfile](recipes/buzzer/Dockerfile) derives a component specific Docker image from one of the [base Docker images](https://github.com/crossbario/crossbar-docker/blob/master/IMAGES.md) we provide for Autobahn based components:


```
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


