# Raspberry Pi and Crossbar.io IoT Starterkit Cookbook

This part of the IoT Cookbook provides information, howtos and [components](components) for the Raspberry Pi and the [Crossbar.io IoT Starterkit](http://crossbario.com/lab/crossbar-iot-starterkit/).


## Installing Docker

The components we provide are run inside Docker containers.

To install Docker, do

```console
curl -sSL https://get.docker.com | sh
```

You also need to be able to run Docker without superuser rights (`sudo`) which can be done like so

```console
sudo usermod -aG docker pi
```

(remember to log back in & out or reboot afterwards for this to take effect).



## Pi Setup: Wi-Fi

You'll often run your Pi headless (controlling it via SSH rather than mouse, keyboard and a monitor).

The following is how you set up Wi-Fi in this case. Additionally, this allows setting up Wi-Fi networks that are not presently in range, and to copy a Wi-Fi configuration across multiple devices.

SSH into the Pi and edit the following file:

```console
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```

For example, here is mine (passwords stripped):

```console
pi@raspberrypi:~ $ sudo cat /etc/wpa_supplicant/wpa_supplicant.conf
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    id_str="office"
    ssid="ap-office"
    psk="********"
    priority=5
}

network={
    id_str="home"
    ssid="ap-home"
    psk="********"
    priority=3
}

network={
    id_str="mobile"
    ssid="ap-mobile"
    psk="********"
    priority=1
}
```

> You can have multiple networks defined, and have priorities on networks as well (when multiple configured networks are in reach). Switching between networks only works for me when rebooting! There are also recipes for making that automatic using some scripts, eg [here](http://raspberrypi.stackexchange.com/questions/11631/how-to-setup-multiple-wifi-networks) - I haven't explored that path yet.

To scan for Wifi networks in reach:

```console
sudo iwlist wlan0 scan
```

To restart Wifi (without reboot):

```console
sudo ifdown wlan0
sudo ifup wlan0
```

To get the current Wifi configuration of the Wifi interface:

```console
ifconfig wlan0
```

To find a Pi on some network:

```console
nmap 192.168.43.*
```

Eg given above, this Pi (MAC `F4:F2:6D:14:1B:56`) will join one of the Wifi network (depending on which one is in reach):

* office: 192.168.1.142
* mobile: 192.168.43.105
* home: 192.168.55.104
