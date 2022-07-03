#!/bin/bash


systemctl enable "monitord-init.service"
systemctl start "monitord-init.service"
systemctl enable "monitord.timer"
systemctl start "monitord.timer"

