PI=pi@raspberrypi.local
IOTCOOKBOOK=${HOME}/scm/crossbario/iotcookbook

login:
	ssh ${PI}

mount:
	dpipe /usr/lib/openssh/sftp-server = ssh ${PI} sshfs :${IOTCOOKBOOK} /home/pi/iotcookbook -o slave &
