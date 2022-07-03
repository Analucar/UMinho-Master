#!/bin/bash

echo 'if $programname == "monitord-logs" then /var/log/monitord-logs.log
& ~' > "/etc/rsyslog.d/monitord-logs.conf"

service rsyslog restart

touch "/etc/monitord-registry.txt" 
cp "monitord.service" "monitord.timer" "monitord-init.service" "/etc/systemd/system/"

touch "/etc/monitord-init.txt"
chmod 600 "/etc/monitord-init.txt"

cp "../src/mon" "/etc/mon"
chmod u+s "/etc/mon"

cp "../src/monitord" "monitord-init.sh" "/opt/"
chmod 700 "/opt/monitord"

systemctl daemon-reload
