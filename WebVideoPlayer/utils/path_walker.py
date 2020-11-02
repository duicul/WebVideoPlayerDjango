'''
Created on Oct 28, 2020

@author: duicul
'''
from pathlib import Path
import os
import re
import uuid
import webvtt
from utils.models import Movie_db,Category_db
import logging
import json
from  django.db.utils import IntegrityError
import django
from imdb import IMDb

logger = logging.getLogger("django")

BASE_DIR = Path(__file__).resolve().parent.parent

def parse_dir(path):
    logger.info("parsing dir : "+str(path))
    main_path=path
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
                    subs=extract_correct_subs(main_path,main_moive_path)
                    video_url="/media/"+os.path.relpath(out_path,start=main_path).replace("\\","/")
                    parent_folder_path=Path(main_moive_path).resolve().parent
                    try:
                        category_db = Category_db(category_path=parent_folder_path,category_name=os.path.basename(parent_folder_path))
                        category_db.save()
                    except django.db.utils.IntegrityError as e:
                        logger.error(e)
                    category_db=Category_db.objects.get(category_path=parent_folder_path)
                    uuid_u= uuid.uuid4()
                    ia = IMDb()
                    movie_imdb = ia.search_movie(main_file_name)
                    logger.info("path_walker : "+str(main_file_name))
                    descr=[]
                    movie_title=""
                    if(len(movie_imdb)>0):
                        mv=ia.get_movie(movie_imdb[0].movieID)
                        movie_title=movie_imdb[0]["title"]
                        try:
                            descr=mv["plot"]
                        except Exception as e:
                            logger.error(e)
                            try:
                                descr=mv["synopsis"]
                            except Exception as e1:
                                logger.error(e1)
                    try:
                        descr_html=""
                        for line in descr:
                            descr_html+=line+"<br/>"
                        movie_db=Movie_db(movie_title=movie_title,name=main_file_name,abs_path=out_path,img_url=img_path,movie_url=video_url,sub_json=json.dumps(subs),unique_id=uuid_u.hex,descr=descr_html,category=category_db)
                        movie_db.save()
                    except Exception as e:
                        logger.error(str(e))

def extract_correct_subs(main_path,main_moive_path):
    subs_path=os.path.join(main_moive_path,"Subs")
    subs=[]
    if not os.path.isdir(subs_path):
        return []
    old_subs_path=os.path.join(subs_path,"old_subs")
    try:
        os.mkdir(old_subs_path)
    except FileExistsError:
        pass
    if(os.path.isdir(subs_path)):
        for sub in os.listdir(subs_path):
            sub_path=os.path.join(subs_path,sub)
            if(os.path.isfile(sub_path)):
                if( sub_path.endswith(".srt")):
                    try:
                        webvtt_sub = webvtt.from_srt(sub_path)
                        webvtt_sub.save()
                    except Exception as e:
                        logger.error(str(e))
                if(not sub_path.endswith(".vtt")):
                    os.rename(sub_path,os.path.join(old_subs_path,sub))  
    
    subs=list(map(lambda x: os.path.relpath(os.path.join(subs_path,x),start=main_path).replace("\\","/"),os.listdir(subs_path)))
    
    subs=list(map(lambda sub_url:"/media/"+str(sub_url),filter(lambda sub:sub.endswith(".vtt"),subs)))
    return subs

def parse_media_dir():
    return parse_dir(os.path.join(BASE_DIR,'media'))
if __name__ == "__main__":
    out=parse_media_dir()
    print(out)