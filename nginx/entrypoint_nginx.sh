#!/bin/bash
set -e
TZ='Europe/Bucharest'; export TZ

pwd > /home/logs/current_dir.log
ls -l > /home/logs/list_workdir.log

FILE=/home/logs/firststart.log

if [ ! -f $FILE ]; then
    date > $FILE
    echo "-- First container startup --"
    cp -r /home/staticinit/* /home/static
else
	date >> /home/logs/additional_run.json
    echo "-- Not first container startup --" >> /home/logs/additional_run.json
fi