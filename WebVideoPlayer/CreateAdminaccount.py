'''
Created on Oct 31, 2020

@author: duicul
'''
import hashlib
import os

import django

import WebVideoPlayer.settings
from utils.models import User_db


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "WebVideoPlayer.settings"
)
django.setup()

if __name__ == '__main__':
    username="admin"
    password="admin"
    text_pass = hashlib.sha512(password.encode())
    encrypt_pass = text_pass.hexdigest()
    user_db=User_db(username=username,password=encrypt_pass)
    user_db.save()