'''
Created on Oct 27, 2020

@author: duicul
'''
import os
myCmd = 'sudo apt install nginx uwsgi uwsgi-plugin-python3'
os.system(myCmd)
myCmd = 'pip3 install django'
os.system(myCmd)
myCmd = 'chmod a+w logs'
os.system(myCmd)
import Createuwsgiconfig
import Createnginxconfig
