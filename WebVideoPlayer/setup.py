'''
Created on Oct 27, 2020

@author: duicul
'''
import os
myCmd = 'sudo apt install nginx uwsgi uwsgi-plugin-python3'
os.system(myCmd)
import Createuwsgiconfig
import Createnginxconfig
