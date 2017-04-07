#!/bin/bash

# /etc/init.d/springboot.sh
# This file allows the app to run in a headless state, runs the app power up
# https://www.cyberciti.biz/tips/linux-how-to-run-a-command-when-boots-up.html

echo "starting main">> /home/pi/log

export PAGERDUTY_API_KEY="key goes here"
export DATADOG_API_KEY="key goes here"
export DATADOG_APP_KEY="key goes here"

# &>> appends, & detaches the process from what’s running it
python3 /home/pi/raspberry-spring/raspberry_spring/main.py &>> /home/pi/log &
