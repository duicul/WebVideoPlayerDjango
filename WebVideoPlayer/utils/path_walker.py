'''
Created on Oct 28, 2020

@author: duicul
'''
from pathlib import Path
import os
import re
import uuid
import webvtt
from utils.models import Movie_db,Category_db,Show_db,Season_db,Episode_db
import logging
import json
from  django.db.utils import IntegrityError
import django
from imdb import IMDb

FORCE_RETRIEVE_IMDB = False

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
                    series_check_path=os.path.join(Path(main_moive_path).resolve().parent.parent,".series")
                    logger.info(series_check_path)
                    series_check=os.path.isfile(series_check_path)
                    logger.info(name+" "+str(series_check))
                    if os.path.isfile(img_path):
                            img_path="/media/"+os.path.relpath(img_path,start=main_path).replace("\\","/")
                    else:
                            img_path="/static/img/not_found.jpg"
                    if(series_check):
                        store_series(main_path,name,main_moive_path,out_path,img_path)
                    else:
                        store_movie(main_path,name,main_moive_path,out_path,img_path)


def store_series(main_path,name,main_moive_path,out_path,img_path):
    main_file_name=name.split(".")
    main_file_name=' '.join(main_file_name[0:len(main_file_name)-1])
    subs=extract_correct_subs(main_path,main_moive_path)
    video_url="/media/"+os.path.relpath(out_path,start=main_path).replace("\\","/")
    season_path=Path(main_moive_path).resolve().parent
    series_path=Path(season_path).resolve().parent
    series_name=os.path.basename(series_path)
    season_name=os.path.basename(season_path)
    series_img_path=os.path.join(series_path,"poster.jpg")
    series_img_path="/media/"+os.path.relpath(series_img_path,start=main_path).replace("\\","/")
    
    season_img_path=os.path.join(season_path,"poster.jpg")
    season_img_path="/media/"+os.path.relpath(season_img_path,start=main_path).replace("\\","/")
    
    categ_path=Path(series_path).resolve().parent
    if categ_path != main_path:
        try:
            category_db = Category_db(category_path=categ_path,category_name=os.path.basename(categ_path))
            logger.info(category_db.getDict())
            category_db.save()
        except django.db.utils.IntegrityError as e:
            logger.error(e) 
            
    if os.path.isfile(series_img_path):
        series_img_path="/media/"+os.path.relpath(series_img_path,start=main_path).replace("\\","/")
    else:
         series_img_path="/static/img/not_found.jpg"
    
    if os.path.isfile(season_img_path):
        series_img_path="/media/"+os.path.relpath(season_img_path,start=main_path).replace("\\","/")
    else:
         series_img_path="/static/img/not_found.jpg"
    
    category_db=Category_db.objects.get(category_path=categ_path)
    try:
        show_db=Show_db(name=series_name,abs_path=series_path,img_url=series_img_path,category=category_db,unique_id=uuid.uuid4().hex)
        logger.info(show_db.getDict())
        show_db.save()
    except django.db.utils.IntegrityError as e:
            logger.error(e)      
    
    show_db=Show_db.objects.get(abs_path=series_path)
    
    season_descr_path=os.path.join(season_path,"descr.json")
    if  not os.path.isfile(season_descr_path) or FORCE_RETRIEVE_IMDB:
        season_descr=create_description_movie(season_descr_path,season_name)
    else:
        desc_file=open(season_descr_path,"r")
        try:
            season_descr=json.load(desc_file)["descr_html"]
        except:
            pass 
    try:
        season_db=Season_db(name=season_name,abs_path=season_path,img_url=season_img_path,show=show_db,descr=season_descr,unique_id=uuid.uuid4().hex)
        logger.info(season_db.getDict())
        season_db.save()
    except django.db.utils.IntegrityError as e:
            logger.error(e)
    
    season_db=Season_db.objects.get(abs_path=season_path)

    episode_desr_path=os.path.join(main_moive_path,"descr.json")
    if  not os.path.isfile(episode_desr_path) or FORCE_RETRIEVE_IMDB:
        episodes=re.findall(r"[Ee](\d+)",main_file_name)
        seasons=re.findall(r"[Ss](\d+)",main_file_name)
        logger.info(main_file_name+" "+str(series_name)+" "+str(seasons)+" "+str(episodes))
        episode_descr=create_description_episode(episode_desr_path,series_name,seasons,episodes)["descr_html"]
        #print(episode_descr)  
    else:
        desc_file=open(episode_desr_path,"r")
        try:
            episode_descr=json.load(desc_file)["descr_html"]
        except Exception as e:
            logger.error(e)
            episode_descr=""
            
    subs=extract_correct_subs(main_path,main_moive_path)    
    
    try:
        episode_db=Episode_db(movie_url=video_url,name=main_file_name,descr=episode_descr,abs_path=main_moive_path,sub_json=subs,season=season_db,unique_id=uuid.uuid4().hex)
        logger.info(episode_db.getDict())
        episode_db.save()
    except django.db.utils.IntegrityError as e:
            logger.error(e)
    
    
    
def store_movie(main_path,name,main_moive_path,out_path,img_path):
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
    logger.info("path_walker : "+str(main_file_name))
    desc_path=os.path.join(main_moive_path,"descr.json")
    if not os.path.isfile(desc_path) or FORCE_RETRIEVE_IMDB:
        desc_data=create_description_movie(desc_path,main_file_name)   
    else:
        desc_file=open(desc_path,"r") 
        desc_data=json.load(desc_file)
    descr_html=desc_data["descr_html"]
    movie_title=desc_data["movie_title"]         
    try:
        movie_db=Movie_db(movie_title=movie_title,name=main_file_name,abs_path=out_path,img_url=img_path,movie_url=video_url,sub_json=json.dumps(subs),unique_id=uuid_u.hex,descr=descr_html,category=category_db)
        movie_db.save()
        logger.info("movie_db : "+str(main_file_name))
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

def create_description_movie(desc_path,main_file_name):
    ia = IMDb()
    movie_imdb = ia.search_movie(main_file_name)
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
    descr_html=""
    for line in descr:
        descr_html+=line+"<br/>"
    
    descr_data={"descr_html":descr_html,"movie_title":movie_title,"search":main_file_name}
    
    desc_file=open(desc_path,"w")
    
    json.dump(descr_data,desc_file)
    
    return descr_data
 
def create_description_episode(desc_path,show,seasons,episodes):
    ia = IMDb()
    movie_title=""
    descr_html=""
    movie_imdb = ia.search_movie(show)
    try:
        if(len(movie_imdb)>0):
            try:
                mv=ia.get_movie(movie_imdb[0].movieID)
                ia.update(mv, 'episodes')
                for season in seasons:
                    for episode in episodes:
                        try:
                            ep=mv['episodes'][int(season)][int(episode)]
                            movie_title+=str(ep["title"])+" <br/>"
                            descr_html+=str(ep["plot"])+" <br/>"
                        except:
                            pass
            except Exception as e:
                logger.error(str(e))
    except Exception as e:
        logger.error(str(e))
    descr_data={"descr_html":descr_html,"movie_title":movie_title,"search":show+" "+str(seasons)+" "+str(episodes)}
    
    desc_file=open(desc_path,"w")
    
    json.dump(descr_data,desc_file)
    logger.info(str(descr_data))
    return descr_data 
    
def parse_media_dir():
    return parse_dir(os.path.join(BASE_DIR,'media'))
if __name__ == "__main__":
    out=parse_media_dir()
    print(out)