#!/bin/bash

while true
do
    netstat -p tcp -na | grep 8000 | grep TIME_WAIT | wc -l | while IFS= read -r line; do
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] $line"
    done
    sleep 1
done