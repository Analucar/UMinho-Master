#!/bin/bash

rm /etc/monitord-registry.txt 
rm /etc/rsyslog.d/monitord-logs.conf
rm /var/log/monitord-logs.log
rm /opt/monitord
rm /etc/systemd/system/monitord.service
rm /etc/systemd/system/monitord-init.service
rm /etc/systemd/system/monitord.timer
rm /etc/mon
rm /etc/monitord-init.txt

systemctl daemon-reload
