# Raspberry Pi and Crossbar.io IoT Starterkit Cookbook

This part of the IoT Cookbook provides information, howtos and [components](components) for the Raspberry Pi and the [Crossbar.io IoT Starterkit](http://crossbario.com/lab/crossbar-iot-starterkit/).


## Enable SSH

Use `sudo raspi-config` to enable remote SSH access to the Pi - see [here](https://www.raspberrypi.org/documentation/remote-access/ssh/).

Then add your public key for password-less login:

```console
ssh pi@192.168.1.136
mkdir ~/.ssh
chmod 700 ~/.ssh
exit
scp /home/oberstet/.ssh/id_rsa.pub pi@192.168.1.136:~/.ssh/authorized_keys
```

## Update the system

To update the system:

```console
sudo apt-get update
sudo apt-get dist-upgrade
sudo apt-get autoremove
sudo reboot
```

## Useful tools

To install some useful tools:

```console
sudo apt-get install -y wget curl vim git htop screen tmux fio glances
```

## Configure Keyboard

The official [docs](https://www.raspberrypi.org/documentation/configuration/raspi-config.md#change-keyboard-layout) don't work for me, but this does:

```console
sudo dpkg-reconfigure keyboard-configuration
```

## Configure Hardware

### SPI and I2C

Enable SPI and I2C by running

```console
sudo raspi-config
```

Go to "Interfacing Options" and make SPI and I2C are enabled.


### Disable Onboard Audio

The onboard Pi audio and the Neopixels boths use PCM hardware and can't be used at the same time. See [here](https://github.com/jgarff/rpi_ws281x#limitations). To disable the onboard audio:

```console
sudo sh -c 'echo "blacklist snd_bcm2835" > /etc/modprobe.d/snd-blacklist.conf'
```

### Check

To check the hardware kernel support modules loaded:

```console
pi@raspberrypi:~ $ lsmod
Module                  Size  Used by
bnep                   12051  2
hci_uart               19956  1
btbcm                   7916  1 hci_uart
bluetooth             365511  22 hci_uart,bnep,btbcm
brcmfmac              222874  0
brcmutil                9092  1 brcmfmac
cfg80211              543027  1 brcmfmac
rfkill                 20851  4 bluetooth,cfg80211
spidev                  7373  0
bcm2835_gpiomem         3940  0
spi_bcm2835             7596  0
i2c_bcm2835             7167  0
evdev                  12423  2
uio_pdrv_genirq         3923  0
uio                    10204  1 uio_pdrv_genirq
fixed                   3285  0
i2c_dev                 6913  0
ipv6                  406279  30
```


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

Remember to log back in & out or reboot afterwards for this to take effect.

Pull some images:

```console
docker pull crossbario/crossbar-armhf
docker pull crossbario/autobahn-js-armhf
docker pull crossbario/autobahn-python-armhf
```


## Check Serial

To get the Pis serial number:

```console
pi@raspberrypi:~ $ cat /proc/cpuinfo | grep Serial
Serial      : 000000005b0966b4
```

## Clone the IoT Cookbook repo

```console
cd ~
git clone https://github.com/crossbario/iotcookbook.git
```

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
