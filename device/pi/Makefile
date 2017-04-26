# export PI=pi@192.168.1.31
# export IOTCOOKBOOK=${HOME}/scm/crossbario/iotcookbook
mount:
	dpipe /usr/lib/openssh/sftp-server = ssh ${PI} sshfs :${IOTCOOKBOOK} /home/pi/iotcookbook -o slave &
