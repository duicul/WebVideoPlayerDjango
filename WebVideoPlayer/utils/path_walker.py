'''
Created on Oct 28, 2020

@author: duicul
'''
from pathlib import Path
import os
import re
import uuid
import webvtt
from utils.models import Movie_db
import logging
import json
logger = logging.getLogger("django")

BASE_DIR = Path(__file__).resolve().parent.parent
#print(BASE_DIR)
def parse_dir(path):
    #print(path)
    #t=[]
    main_path=path
    #print(main_path)
    exten = ['.mp4','.avi','.m3u8']
    for dirpath, dirnames, files in os.walk(path,followlinks=True):
        for name in files:
            for ext in exten:
                if name.lower().endswith(ext):
                    out_path=os.path.join(dirpath, name)
                    main_moive_path=Path(out_path).resolve().parent.parent if ext == ".m3u8" else Path(out_path).resolve().parent
                    img_path=os.path.join(main_moive_path,"poster.jpg")
                    if not os.path.isfile(img_path):
                        img_path="/static/img/not_found.jpg"
                    else:
                        img_path="/media/"+os.path.relpath(img_path,start=main_path).replace("\\","/")
                    main_file_name=name.split(".")
                    main_file_name=''.join(main_file_name[0:len(main_file_name)-1])
                    subs_path=os.path.join(main_moive_path,"Subs")
                    subs=[]
                    subs_names=[]
                    print("subs_path "+str(subs_path))
                    if(os.path.isdir(subs_path)):
                        for sub in os.listdir(subs_path):
                            sub_path=os.path.join(subs_path,sub)
                            if(os.path.isfile(sub_path) and sub_path.endswith(".srt")):
                                #print(sub_path)
                                webvtt_sub = webvtt.from_srt(sub_path)
                                #os.remove(sub_path) 
                                #print(sub_path)
                                webvtt_sub.save()
                    if(os.path.isdir(subs_path)):
                        subs=list(map(lambda x: os.path.relpath(os.path.join(subs_path,x),start=main_path).replace("\\","/"),os.listdir(subs_path)))
                    subs=list(map(lambda sub_url:"/media/"+str(sub_url),filter(lambda sub:sub.endswith(".vtt"),subs)))
                    #print(main_file_name)
                    #print(img_path)
                    video_url="/media/"+os.path.relpath(out_path,start=main_path).replace("\\","/")
                    #new_entry={"name":main_file_name,"img_url":img_path,"movie_url":video_url}
                    #print(new_entry)
                    #t.append(new_entry)
                    uuid_u= uuid.uuid4()
                    try:
                        movie_db=Movie_db(name=main_file_name,abs_path=out_path,img_url=img_path,movie_url=video_url,sub_json=json.dumps(subs),unique_id=uuid_u.hex)
                        movie_db.save()
                    except Exception as e:
                        logger.error(str(e))
    #return t

def parse_media_dir():
    return parse_dir(os.path.join(BASE_DIR,'media'))
if __name__ == "__main__":
    out=parse_media_dir()
    print(out)