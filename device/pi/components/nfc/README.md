# Crossbar.io IoT Starterkit - NFC 

Using _ST M24SR64_ NFC Device as a WAMP - component based on a Arduino library for communication over I2C

First: try to write and read NDEF - Message from this chip with a ACS ACR122U-A9 NFC-Card Reader/Writer

## Install driver for ACR122

in referece to a guide found [here](https://oneguyoneblog.com/2016/11/02/acr122u-nfc-usb-reader-linux-mint/)

1. First install pcps tools

```console
sudo apt-get install pcscd pcsc-tools
```
2. got to ```sudo nano /etc/modprobe.d/blacklist.conf``` and blacklist _nfc_ and the _pn533_ modules by adding followed code at the bottom of the file:
```console
blacklist nfc
blacklist pn533
blacklist pn533_usb
```
3. download the driver for the ARC122 from the [Advanced Card Systems website](http://www.acs.com.hk/en/products/3/acr122u-usb-nfc-reader/)
4. exctract the downloaded archive 
5. go to _ACS-Unified-PKG-Lnx-113-P/acsccid_linux_bin-1.1.3/ubuntu/trusty_ and run for x64-bit
```console
sudo dpkg -i libacsccid1_1_xxxxx64.deb
```
>Note: the xxxs in that command are standing for your individual version number
>
6. now you have to reboot your _pcscd-service_ or just reboot your computer
```console
sudo service pcscd restart
sudo modprobe pn533_usb
sudo modprobe pn533
```
7. now you should install _nfc-tools_ by running

```console
sudo apt-get install libnfc-dev
```

8. at this moment it is time to look if you can find your NFC-Reader 
```console
nfc-list
```
9. if should get something like this your installation was successful

```console
nfc-list uses libnfc 1.7.1
NFC device: ACS / ACR122U PICC Interface opened
1 ISO14443A passive target(s) found:
ISO/IEC 14443A (106 kbps) target:
    ATQA (SENS_RES): 00  42  
       UID (NFCID1): 02  84  00  17  df  7d  99  
      SAK (SEL_RES): 20  
                ATS: 78  00  50  02  
```

# Building an NDEF message with _ndeftool_
> Full Documentation: https://ndeftool.readthedocs.io/en/latest/
1. install ndeftool with 
```console
pip install ndeftool
```
 2. now you are able to build and read NDEF messages. 
 for example: 
 ```console
text "Crossbar-Website" id "r1" uri "http://crossbar.io" save -k "message.ndef" print
```
 - it will create a NDEF-message with two records in it
   - one textrecord containing "Crossbar-Website"
   - one URI pointing to "http://crossbar.io"
- it will save the file at your local folder 
- it will print the attributes in a readable way
 >Please read the manual for more information
 # Writing the NDEF message on your NFC tag
> Full documentation: http://nfcpy.readthedocs.io/en/latest/examples/tagtool.html
1. clone the _nfcpy_ - repo at a folder of your choise with
```console
git clone git@github.com:nfcpy/nfcpy.git
```
2. go to ```../nfcpy/examples/```
3. copy here your message file you've builded before
4. write the NDEF-message on your tag with
```console
./tagtool.py load message.ndef
```
if you see something like this your writing process was sucessful
```console

[nfc.clf] searching for reader on path usb
[nfc.clf] using ACS ACR122U PN532v1.6 at usb:002:003
** waiting for a tag **
[nfc.tag.tt4] ACS ACR122U on usb:002:003 does not support fsd 256
[nfc.tag.tt4] ACS ACR122U on usb:002:003 does not support fsc 256
Old message:
record 1
  type   = 'urn:nfc:wkt:U'
  name   = ''
  data   = '\x03google.de'
New message:
record 1
  type   = 'urn:nfc:wkt:U'
  name   = ''
  data   = '\x00crossbar.io'
record 2
  type   = 'urn:nfc:wkt:T'
  name   = ''
  data   = '\x02enCrossbar-Website'
```
# Reading a NDEF message from your NFC tag
1. we can use the same to read from the tag and write it in a file 
```console
./tagtool.py dump -o message.ndef
```
2. get the NDEF information in a quite pretty way
```console
ndeftool l Dump2.ndef print
```

## Using Arduino Library 
in this section a Arduino library is used to communicate over _I2C_-Bus and write a NDEF - Message to the _ST M24SR64_ 
> Library can be found [here](https://github.com/rena2019/ArduinoM24SR)
>

Debuging Serial print for initialization and writing : 
```console
_setup

writeGPO

verifyI2cPassword

selectFile_NDEF_App

sendApdu
GetI2Csession: 0
=> 
StartTransmission: 02 00 A4 04 00 07 D2 76 00 00 85 01 01 A609

receiveResponse, len=5
<= 03 90 00 2D 53 
sendApdu
GetI2Csession: 0
=> 
StartTransmission: 03 00 20 00 03 10 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 0382

receiveResponse, len=5
<= 02 90 00 F1 09 Password passed

sendApdu
GetI2Csession: 0
=> 
StartTransmission: 02 00 A4 00 0C 02 E1 01 7F0D

receiveResponse, len=5
<= 03 90 00 2D 53 
GetI2Csession: 0
=> 
StartTransmission: 03 00 D6 00 04 01 61 D0E3

receiveResponse, len=5
<= 02 90 00 F1 09 
send DESELECT
GetI2Csession: 0
=> 
StartTransmission: C2 E0B4

receiveResponse, len=3
<= C2 E0 B4 
free RAM: 6476

free RAM: 6277

NDEF Message 3 records, 71 bytes
  NDEF Record
    TNF 0x1 Well Known
    Type Length 0x1 1
    Payload Length 0x13 19
    Type 55  U
    Payload 00 68 74 74 70 3A 2F 2F 63 72 6F 73 73 62 61 72 2E 69 6F  .http://crossbar.io
    Record is 23 bytes
  NDEF Record
    TNF 0x1 Well Known
    Type Length 0x1 1
    Payload Length 0x13 19
    Type 55  U
    Payload 00 68 74 74 70 3A 2F 2F 63 72 6F 73 73 62 61 72 2E 69 6F  .http://crossbar.io
    Record is 23 bytes
  NDEF Record
    TNF 0x1 Well Known
    Type Length 0x1 1
    Payload Length 0x15 21
    Type 54  T
    Payload 02 65 6E 68 74 74 70 3A 2F 2F 63 72 6F 73 73 62 61 72 2E 69 6F  .enhttp://crossbar.io
    Record is 25 bytes
NDefRecord:   NDEF Record
    TNF 0x1 Well Known
    Type Length 0x1 1
    Payload Length 0x13 19
    Type 55  U
    Payload 00 68 74 74 70 3A 2F 2F 63 72 6F 73 73 62 61 72 2E 69 6F  .http://crossbar.io
    Record is 23 bytes

selectFile_NDEF_App

sendApdu
GetI2Csession: 0
=> 
StartTransmission: 02 00 A4 04 00 07 D2 76 00 00 85 01 01 A609

receiveResponse, len=5
<= 02 90 00 F1 09 
selectFile_NDEF_file
GetI2Csession: 0
=> 
StartTransmission: 03 00 A4 00 0C 02 00 01 817C

receiveResponse, len=5
<= 03 90 00 2D 53 
updateBinary_NdefMsgLen0
GetI2Csession: 0
=> 
StartTransmission: 02 00 D6 00 00 02 00 00 D4B6

receiveResponse, len=5
<= 02 90 00 F1 09 
updateBinary
91 01 13 55 00 68 74 74 70 3A 2F 2F 63 72 6F 73 
73 62 61 72 2E 69 6F 11 01 13 55 00 68 74 74 70 
3A 2F 2F 63 72 6F 73 73 62 61 72 2E 69 6F 51 01 
15 54 02 65 6E 68 74 74 70 3A 2F 2F 63 72 6F 73 
73 62 61 72 2E 69 6F 
chunk_len:24, pos:0
GetI2Csession: 0
=> 
StartTransmission: 03 00 D6 00 02 18 91 01 13 55 00 68 74 74 70 3A 2F 2F 63 72 6F 73 73 62 61 72 2E 69 6F 11 3D72

receiveResponse, len=5
<= F2 02 0A 72 
WTX
GetI2Csession: 0
=> 
StartTransmission: F2 02 0A72
<= 
chunk_len:24, pos:24
GetI2Csession: 0
=> 
StartTransmission: 02 00 D6 00 1A 18 01 13 55 00 68 74 74 70 3A 2F 2F 63 72 6F 73 73 62 61 72 2E 69 6F 51 01 0037

receiveResponse, len=5
<= F2 03 83 63 
WTX
GetI2Csession: 0
=> 
StartTransmission: F2 03 8363
<= 
chunk_len:23, pos:48
GetI2Csession: 0
=> 
StartTransmission: 03 00 D6 00 32 17 15 54 02 65 6E 68 74 74 70 3A 2F 2F 63 72 6F 73 73 62 61 72 2E 69 6F 8235

receiveResponse, len=5
<= F2 02 0A 72 
WTX
GetI2Csession: 0
=> 
StartTransmission: F2 02 0A72
<= 
updateBinaryLen

GetI2Csession: 0
=> 
StartTransmission: 02 00 D6 00 00 02 00 47 6F80

receiveResponse, len=5
<= 02 90 00 F1 09 
send DESELECT
GetI2Csession: 0
=> 
StartTransmission: C2 E0B4

receiveResponse, len=3
<= C2 E0 B4 
```
Next step should be analyzing the _I2C_ - messages with the Datasheet to get a I2C - session working with the raspberry pi
 