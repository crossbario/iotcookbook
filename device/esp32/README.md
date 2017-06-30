# ESP32

The ESP32 is a low-power Wifi/BL(E) module priced below 3 US-$.

## Requirements

To work with the examples posted on this page you first have to install the ESP Toolchain and the ESP SDK on your system:

1. [install the toolchain](https://esp-idf.readthedocs.io/en/latest/get-started/index.html#standard-setup-of-toolchain)
2. [install the SDK](https://esp-idf.readthedocs.io/en/latest/get-started/index.html#get-esp-idf)

Here is my setup

```console
oberstet@thinkpad-t430s:~/esp$ ll
insgesamt 16
drwxrwxr-x  4 oberstet oberstet 4096 Jun 30 12:41 ./
drwxr-xr-x 88 oberstet oberstet 4096 Jun 30 12:43 ../
drwxrwxr-x  8 oberstet oberstet 4096 Jun 30 12:41 esp-idf/
drwxrwxr-x  8 oberstet oberstet 4096 Jan 11 06:17 xtensa-esp32-elf/
oberstet@thinkpad-t430s:~/esp$ grep esp ~/.profile 
export PATH=${PATH}:${HOME}/esp/xtensa-esp32-elf/bin
export IDF_PATH=${HOME}/esp/esp-idf
oberstet@thinkpad-t430s:~/esp$ 
```

Further, to be able to flash from a non-root user:

```console
sudo usermod -a -G dialout $USER
```

To flash and monitor:

```console
make flash monitor
```

and to stop/exit:

```
```console
--- idf_monitor on /dev/ttyUSB0 115200 ---
--- Quit: Ctrl+] | Menu: Ctrl+T | Help: Ctrl+T followed by Ctrl+H ---
```
