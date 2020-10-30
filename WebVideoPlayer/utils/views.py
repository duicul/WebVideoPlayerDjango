from django.shortcuts import render
from django.http import HttpResponse
import os
import json
import sys
from utils.LoginForm import LoginForm
from utils.path_walker import parse_media_dir
from utils.models import User_db
import video_player
from django.http import HttpResponseRedirect
import WebVideoPlayer
import utils
import hashlib
#import video_player_utils
# Create your views here.
def list_dir(request):
    try:
       path=request.GET.get("path")
    except:
        path=""
    print("list_dir "+str(path))
    t={}
    if path==None or len(path)==0:
        if sys.platform=="win32":
            import win32api
            drives = win32api.GetLogicalDriveStrings()
            drives = drives.split('\000')[:-1]
            t=list(map(lambda x:x.replace("\n",""),drives))
        elif sys.platform=="linux1" or sys.platform=="linux2":
            t=list(map(lambda x:x.replace("\n",""),os.listdir("/")))
    else:
        t=list(map(lambda x:x.replace("\n",""),os.listdir(path)))
    return HttpResponse(json.dumps(t), content_type="application/json")

def list_video_files(request):
    dirs=parse_media_dir()
    return HttpResponse(json.dumps(dirs), content_type="application/json")

def login(request):
    username=None
    password=None
    MyLoginForm=None
    if request.method == 'POST':
        MyLoginForm = LoginForm(request.POST)
    elif request.method == 'GET':
        MyLoginForm = LoginForm(request.GET)
    if MyLoginForm.is_valid() and not MyLoginForm == None:
        username = MyLoginForm.cleaned_data["username"]
        password = MyLoginForm.cleaned_data["password"]
    if not ( username == None or password == None):
        text_pass = hashlib.sha512(password.encode())
        encrypt_pass = text_pass.hexdigest()
        user_db=User_db.objects.filter(username = username)
        print("user_db "+str(user_db))
        if len(user_db)>0 and encrypt_pass == user_db[0].password:
            request.session['username']=username
            return HttpResponseRedirect("/")
    return HttpResponseRedirect("/?login=wrong")
            
def register(request):
    username=None
    password=None
    MyLoginForm=None
    if request.method == 'POST':
        MyLoginForm = LoginForm(request.POST)
        if MyLoginForm.is_valid() and not MyLoginForm == None:
            username = MyLoginForm.cleaned_data["username"]
            password = MyLoginForm.cleaned_data["password"]
    elif request.method == 'GET':
        username=request.GET.get("username")
        password=request.GET.get("password")
    if not ( username == None or password == None):
        text_pass = hashlib.sha512(password.encode())
        encrypt_pass = text_pass.hexdigest()
        user_db=User_db(username=username,password=encrypt_pass)
        user_db.save()
        print("register "+str(username)+" "+str(password)+" "+encrypt_pass)
    return HttpResponseRedirect("/")
    
def logout(request):
    try:
        del request.session['username']
    except:
        pass
    video_player.views.index(request)
    return HttpResponseRedirect("/")