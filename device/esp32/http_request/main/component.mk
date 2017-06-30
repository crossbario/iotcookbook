#
# Main component makefile.
#
# This Makefile can be left empty. By default, it will take the sources in the
# src/ directory, compile them and link them into lib(subdirectory_name).a
# in the build directory. This behaviour is entirely configurable,
# please read the ESP-IDF documents if you need to do this.
#
CFLAGS += -DWIFI_SSID_VALUE=\"${WIFI_SSID}\"
CFLAGS += -DWIFI_KEY_VALUE=\"${WIFI_KEY}\"
CFLAGS += -DWEB_SERVER=\"${CROSSBAR_SERVER}\"
CFLAGS += -DWEB_PORT=\"${CROSSBAR_PORT}\"
CFLAGS += -DWEB_URL=\"${CROSSBAR_URL}\"
