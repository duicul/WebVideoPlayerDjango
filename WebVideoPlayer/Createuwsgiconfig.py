'''
Created on Oct 27, 2020

@author: duicul
'''
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)
str_out="[uwsgi] \nchdir = "
str_out+=BASE_DIR
str_out+="\n"
str_out+="plugins = python3\n"
str_out+="module=WebVideoPlayer.wsgi:application\n"
str_out+="env = 'DJANGO_SETTINGS_MODULE=WebVideoPlayer.settings' # customize with your settings module \n"
str_out+="wsgi-file = WebVideoPlayer/wsgi.py # customize with the relative path to your wsgi.py file \n"

str_out+="workers = 1"
f = open("/etc/uwsgi/apps-enabled/django.ini", "w")
f.write(str_out)
f.close()
myCmd = 'service uwsgi restart'
os.system(myCmd)