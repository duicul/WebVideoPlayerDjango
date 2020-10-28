from django.shortcuts import render
from django.http import HttpResponse
import os
import json
import sys
from utils.path_walker import parse_media_dir
#import video_player_utils
# Create your views here.
def list_dir(request):
    try:
       path=request.GET.get("path")
    except:
        path=""
    print(path)
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
