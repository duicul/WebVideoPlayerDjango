from django.shortcuts import render
from django.http import HttpResponse
import os
import json
import sys

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

import re
 
def list_video_files(request):
    try:
       path=request.GET.get("path")
    except:
        path=""
    print("./media")
    # The top argument for walk
    path="./media"
    topdir = '.'
    # The extension to search for
    exten = ['.mp4','.avi']
    t=[]
    main_dir=os.listdir(path)
    print(main_dir)
    for dirpath, dirnames, files in os.walk(topdir):
        for name in files:
            for ext in exten:
                if name.lower().endswith(ext):
                    print(name)
                    print(dirnames)
                    print(os.path.join(dirpath, name))
                    #t.append(os.path.join(dirpath, name))
                    out_path=os.path.join(dirpath, name)
                    print(re.sub(r'^\.\\','',out_path))
                    t.append(re.sub(r'^\.\\','',out_path))
    return HttpResponse(json.dumps(t), content_type="application/json")
