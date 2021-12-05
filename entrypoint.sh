#!/bin/bash
set -e
TZ='Europe/Bucharest'; export TZ

pwd > /home/logs/current_dir.log
ls -l > /home/logs/list_workdir.log

FILE=/home/logs/firststart.log

if [ ! -f $FILE ]; then
    date > $FILE
    echo "-- First container startup --"
	rm /home/jsoninit/config_weather.json
	rm /home/json/config_weather.json
    cp -r /home/dbinit/*.db /home/db
	cp -r /home/jsoninit/*.json /home/json
else
	date >> /home/logs/additional_run.json
    echo "-- Not first container startup --" >> /home/logs/additional_run.json
fi

#cd db;ls -l > /home/logs/list_dbdir.log;cd ..;
#cd json;ls -l > /home/logs/list_jsondir.log;cd ..;
echo "----- Collect static files ------ " 
python manage.py collectstatic --noinput

echo "-----------Apply migration--------- "
python manage.py makemigrations 
python manage.py migrate

echo "-----------Run gunicorn--------- "
uwsgi djangoWebPlayer.ini
#gunicorn --bind 0.0.0.0:7700 WebVideoPlayer.wsgi --workers 4 --log-level=info