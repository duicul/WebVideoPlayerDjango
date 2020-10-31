from django.shortcuts import render
from django.http import HttpResponse
import os
import json
import sys
from utils.LoginForm import LoginForm
from utils.path_walker import parse_media_dir
from utils.models import User_db,Movie_db
import video_player
from django.http import HttpResponseRedirect
import hashlib
import logging
from django.core.exceptions import PermissionDenied
from utils.FileUploadForm import FileUploadForm
from utils.FileUploadHandling import handle_uploaded_file
logger = logging.getLogger("django")

# Create your views here.
def file_upload_form(request):
    username=None
    login=None
    try:
        username=request.session['username']
    except KeyError:
        raise PermissionDenied()
    try:
        uploaded=request.GET.get("uploaded")
    except KeyError:
        uploaded=None
    form=FileUploadForm()
    return render(request,"file_upload.html",{"uploaded":uploaded,"form":form})

def list_dir(request):
    try:
       path=request.GET.get("path")
    except:
        path=""
    #print("list_dir "+str(path))
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
    username=None
    try:
        username=request.session['username']
    except KeyError:
        raise PermissionDenied()
    return HttpResponse(json.dumps([mv.getDict() for mv in Movie_db.objects.all()]), content_type="application/json")
    
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
        #print("user_db "+str(user_db))
        if len(user_db)>0 and encrypt_pass == user_db[0].password:
            request.session['username']=username
            return HttpResponseRedirect("/")
    return HttpResponseRedirect("/?login=wrong")
            
def register(request):
    logged_user=None
    try:
        logged_user=request.session['username']
    except KeyError:
        raise PermissionDenied() 
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
        #print("register "+str(username)+" "+str(password)+" "+encrypt_pass)
    return HttpResponseRedirect("/")

def rescan_db(request):
    logged_user=None
    try:
        logged_user=request.session['username']
    except KeyError:
        raise PermissionDenied()
    Movie_db.objects.all().delete()
    parse_media_dir()
    logger.info("scan_db")
    return HttpResponse()

def logout(request):
    try:
        del request.session['username']
    except:
        pass
    video_player.views.index(request)
    return HttpResponseRedirect("/")

def list_users(request):
    logged_user=None
    try:
        logged_user=request.session['username']
    except KeyError:
        raise PermissionDenied() 
    return HttpResponse(json.dumps([user.getDict() for user in User_db.objects.all()]), content_type="application/json")


def upload_file(request):
    logger.info(" file upload ")
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        logger.info("file upload form valid : "+str(form.is_valid()))
        logger.info("file upload form erros : "+str(form.errors.as_data()))
        #logger.info(str(form))
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'],form.cleaned_data["folder"])
            return HttpResponseRedirect('/file_upload_form')
        return HttpResponseRedirect('/file_upload_form?uploaded=wrong')
    else:
        return HttpResponseRedirect('/file_upload_form?uploaded=wrong')
    #return render(request, 'upload.html', {'form': form})