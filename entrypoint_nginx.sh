#!/bin/bash
set -e
TZ='Europe/Bucharest'; export TZ

FILE=/home/logs/firststart.log

if [ ! -f $FILE ]; then
    date > $FILE
    echo "-- First container startup --"
    cp -r /home/staticinit/* /home/static
else
    echo "-- Not first container startup --"
fi