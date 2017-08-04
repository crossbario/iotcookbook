#
# This is a project Makefile. It is assumed the directory this Makefile resides in is a
# project subdirectory.
#

PROJECT_NAME := hello-world

BATCH_BUILD=1
include $(IDF_PATH)/make/project.mk


build:
	sudo docker build --rm -t esp32 .

esp32:
	 docker run \
	--device=/dev/ttyUSB0 \
	-v ${shell pwd}:/home/app \
	-it esp32 \
	-e CROSSBAR_HTTP_BRIDGE \
	-e WIFI_KEY \
	-e WIFI_SSID \
	make -j5   # build the project

esp32_monitor:
	 docker run \
	--device=/dev/ttyUSB0 \
	-v ${shell pwd}:/home/app \
	-it esp32 \
	make monitor # execute the monitor

esp32_flash:
	 docker run \
	--device=/dev/ttyUSB0 \
	-v ${shell pwd}:/home/app \
	-e CROSSBAR_HTTP_BRIDGE \
	-e WIFI_KEY \
	-e WIFI_SSID \
	-it esp32 \
	make flash  # flash the program to the chip

esp32_all:
	 docker run \
	--device=/dev/ttyUSB0 \
	-v ${shell pwd}:/home/app \
	-e WIFI_KEY \
	-e CROSSBAR_HTTP_BRIDGE \
	-e WIFI_SSID \
	-it esp32 \
	make -j5 flash monitor  # build and flash the program and load the monitor

esp32_bash:
	 docker run \
	--device=/dev/ttyUSB0 \
	-v ${shell pwd}:/home/app \
	-e WIFI_KEY \
	-e CROSSBAR_HTTP_BRIDGE \
	-e WIFI_SSID \
	-it esp32
