#!/bin/bash

systemctl stop "monitord-init.service"
systemctl disable "monitord-init.service"
systemctl stop "monitord.timer"
systemctl disable "monitord.timer"
systemctl stop "monitord.service"
systemctl disable "monitord.service"
systemctl daemon-reload
