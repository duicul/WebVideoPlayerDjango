'''
Created on Oct 30, 2020

@author: duicul
'''
import os

myCmd = 'service uwsgi restart'
os.system(myCmd)
myCmd = 'service nginx restart'
os.system(myCmd)