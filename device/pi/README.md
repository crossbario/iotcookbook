# Raspberry Pi and Crossbar.io IoT Starterkit Cookbook

This part of the IoT Cookbook provides information, howtos and recipes for the Raspberry Pi and the Crossbar.io IoT Starterkit.

Running the recipes here is only three commands, eg here is how to start the [Buzzer Recipe](recipes/buzzer):

```console
ssh pi@raspberrypi.local
git clone https://github.com/crossbario/iotcookbook.git
cd iotcookbook/device/pi/recipes/buzzer
make start
```

> This assumes you have a Linux with Docker running on the Pi, eg Raspbian with Docker.

The `make start` command will first build a Docker image named `cookbook-buzzer`:

```console
docker build -t cookbook-buzzer -f Dockerfile .
```

The `Dockerfile` derives a component specific Docker image from one of the [base Docker images](https://github.com/crossbario/crossbar-docker/blob/master/IMAGES.md) we provide for Autobahn based components:


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

Finally, the example `/app/*` contents that comes with our base images is replaced with our buzzer application code, everything from the `app` folder on the build host, and the image is configured to start `client.py` by default using Python.

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
