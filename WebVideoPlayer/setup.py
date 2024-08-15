'''
Created on Oct 27, 2020

@author: duicul
'''
import os

import CreateAdminaccount
import Createnginxconfig
import Createuwsgiconfig
import restartServices

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
myCmd = 'mkdir '+BASE_DIR+'/logs;chmod a+w '+BASE_DIR+'/logs;'
os.system(myCmd)
myCmd = 'sudo apt install nginx uwsgi uwsgi-plugin-python3'
os.system(myCmd)
myCmd = 'pip3 install python3-django'
os.system(myCmd)
myCmd = 'pip3 install python3-cinemagoer'
os.system(myCmd)
myCmd = 'pip3 install python3-webvtt-py'
os.system(myCmd)
myCmd = 'pip3 install python3-psutil'
os.system(myCmd)
myCmd = 'chmod a+w .'
os.system(myCmd)
myCmd = 'chmod a+w ..'
os.system(myCmd)
myCmd = 'chmod a+w logs'
os.system(myCmd)
myCmd = 'python3 manage.py makemigrations'
os.system(myCmd)
myCmd = 'python3 manage.py migrate'
os.system(myCmd)
myCmd = 'chmod a+w ./*'
os.system(myCmd)
myCmd = 'chmod a+w ../*'
os.system(myCmd)
