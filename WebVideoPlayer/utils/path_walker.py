'''
Created on Oct 28, 2020

@author: duicul
'''
import os

import django
import imdb
import webvtt

import json
import logging
from pathlib import Path
import re
import traceback
from utils.models import Movie_db, Category_db, Show_db, Season_db, Episode_db
import uuid


FORCE_RETRIEVE_IMDB = False

logger = logging.getLogger("django")

BASE_DIR = Path(__file__).resolve().parent.parent

imdb_cache = {"show":{}, "movie":{}}
imdb_cache_id = {"show":{}, "movie":{}}
try:
    logger.info("path_walker creating cinemagoer instance")
    ia = imdb.Cinemagoer()
except:
    logger.error(str(traceback.format_exc()))
    ia = None

    
def clean_db_tables():
    categs = Category_db.objects.all()
    for cat in categs:
        if not os.path.isdir(cat.category_path):
            logger.info("delete category " + str(cat.category_path))
            cat.delete()
            
    mvs = Movie_db.objects.all()
    for mv in mvs:
        if not os.path.isfile(mv.abs_path):
            logger.info("delete movie " + str(mv.abs_path))
            mv.delete()
            
    shs = Show_db.objects.all()
    for sh in shs:
        if not os.path.isdir(sh.abs_path):
            logger.info("delete show " + str(sh.abs_path))
            sh.delete()
    
    seasons = Season_db.objects.all()
    for seas in seasons:
        if not os.path.isdir(seas.abs_path):
            logger.info("delete season " + str(seas.abs_path))
            seas.delete()
    
    eps = Episode_db.objects.all()
    for ep in eps:
        if not os.path.isfile(ep.abs_path):
            logger.info("delete episode " + str(ep.abs_path))
            ep.delete()


def filenamewithoutext(filename):
    filenamelist = os.path.splitext(filename)
    filenamelist = filenamelist[:len(filenamelist) - 1]
    retname = ""
    for part in filenamelist:
        retname += part
    return retname    


def parse_dir(path):
    logger.info("parsing dir : " + str(path))
    main_path = path
    exten = ['.m3u8','.mp4', '.avi']
    for dirpath, dirnames, files in os.walk(path, followlinks=True):
        for name in files:
            for ext in exten:
                if name.lower().endswith(ext) and not "vtt" in name.lower():
                    out_path = os.path.join(dirpath, name)
                    main_moive_path = Path(out_path).resolve().parent.parent if ext == ".m3u8" else Path(out_path).resolve().parent
                    img_path = os.path.join(main_moive_path, "poster.jpg")
                    series_check_path = os.path.join(Path(main_moive_path).resolve().parent.parent, ".series")
                    logger.info(series_check_path)
                    series_check = os.path.isfile(series_check_path)
                    logger.info(name + " " + str(series_check))
                    if os.path.isfile(img_path):
                            img_path = "/media/" + os.path.relpath(img_path, start=main_path).replace("\\", "/")
                    else:
                            img_path = "/static/img/not_found.jpg"
                    try:
                        
                        vtt_m3u8_subPath = os.path.join(dirpath, filenamewithoutext(name) + "_vtt.m3u8")
                        if not os.path.isfile(vtt_m3u8_subPath):
                            vtt_m3u8_subPath = None
                        if(series_check):
                            store_series(main_path, name, main_moive_path, out_path, img_path, vtt_m3u8_subPath)
                        else:
                            store_movie(main_path, name, main_moive_path, out_path, img_path, vtt_m3u8_subPath)
                    except:
                        logger.error(str(traceback.format_exc()))
                    
                    break

def store_series(main_path, name, main_moive_path, out_path, img_path, vtt_m3u8_subPath):
    main_file_name = name.split(".")
    main_file_name = ' '.join(main_file_name[0:len(main_file_name) - 1])
    video_url = "/media/" + os.path.relpath(out_path, start=main_path).replace("\\", "/")
    season_path = Path(main_moive_path).resolve().parent
    series_path = Path(season_path).resolve().parent
    series_name = os.path.basename(series_path)
    season_name = os.path.basename(season_path)
    series_img_path = os.path.join(series_path, "poster.jpg")
    series_img_path = "/media/" + os.path.relpath(series_img_path, start=main_path).replace("\\", "/")
    
    season_img_path = os.path.join(season_path, "poster.jpg")
    season_img_path = "/media/" + os.path.relpath(season_img_path, start=main_path).replace("\\", "/")
    
    categ_path = Path(series_path).resolve().parent
    if categ_path != main_path:
        try:
            category_db = Category_db.objects.get(category_path=categ_path)
            category_db.category_name = os.path.basename(categ_path)
            category_db.save()
        except Category_db.DoesNotExist as e:
            logger.error(e) 
            try:
                category_db = Category_db(category_path=categ_path, category_name=os.path.basename(categ_path))
                category_db.save()
            except django.db.utils.IntegrityError as e:
                logger.error(e) 
                
    logger.info(category_db.getDict())
            
    if os.path.isfile(series_img_path):
        series_img_path = "/media/" + os.path.relpath(series_img_path, start=main_path).replace("\\", "/")
    else:
         series_img_path = "/static/img/not_found.jpg"
    
    if os.path.isfile(season_img_path):
        series_img_path = "/media/" + os.path.relpath(season_img_path, start=main_path).replace("\\", "/")
    else:
         series_img_path = "/static/img/not_found.jpg"
    
    try:
            show_db = Show_db.objects.get(abs_path=series_path)
            show_db.name = series_name
            show_db.img_url = series_img_path
            show_db.category = category_db
            show_db.save()
    except Show_db.DoesNotExist as e:
        logger.error(e) 
        try:
            show_db = Show_db(name=series_name, abs_path=series_path, img_url=series_img_path, category=category_db, unique_id=uuid.uuid4().hex)
            show_db.save()
        except django.db.utils.IntegrityError as e:
            logger.error(e)      
    
    logger.info(show_db.getDict())
    
    season_descr_path = os.path.join(season_path, "descr.json")
    if  not os.path.isfile(season_descr_path) or FORCE_RETRIEVE_IMDB:
        season_descr = create_description_movie(season_descr_path, season_name)
    else:
        desc_file = open(season_descr_path, "r")
        try:
            season_descr = json.load(desc_file)["descr_html"]
        except:
            pass 
    try:
        season_db = Season_db.objects.get(abs_path=season_path)
        season_db.name = season_name
        season_db.img_url = season_img_path
        season_db.show = show_db
        season_db.descr = season_descr
        season_db.save()
    except Season_db.DoesNotExist as e:
        logger.error(e) 
        try:
            season_db = Season_db(name=season_name, abs_path=season_path, img_url=season_img_path, show=show_db, descr=season_descr, unique_id=uuid.uuid4().hex)
            season_db.save()
        except django.db.utils.IntegrityError as e:
            logger.error(e)
    
    logger.info(season_db.getDict())

    episode_desr_path = os.path.join(main_moive_path, "descr.json")
    if  not os.path.isfile(episode_desr_path) or FORCE_RETRIEVE_IMDB:
        episodes = re.findall(r"[Ee](\d+)", main_file_name)
        seasons = re.findall(r"[Ss](\d+)", main_file_name)
        seriesName = re.search(r"(.+) *(S[0-9]?[0-9]?.*E[0-9]?[0-9]?)", main_file_name).group(1)
        logger.info(main_file_name + " " + str(seriesName) + " " + str(seasons) + " " + str(episodes))
        episode_descr = create_description_episode(episode_desr_path, seriesName, seasons, episodes)
        # print(episode_descr)  
    else:
        desc_file = open(episode_desr_path, "r")
        try:
            episode_descr = json.load(desc_file)
        except Exception as e:
            logger.error(e)
            episode_descr = ""
            
    subs = json.dumps(extract_correct_subs(main_path, main_moive_path, vtt_m3u8_subPath))    
    logger.info("extract_correct_subs episode " + str(subs))
    try:
        episode_db = Episode_db.objects.get(abs_path=out_path)
        episode_db.movie_url = video_url
        episode_db.name = main_file_name
        episode_db.movie_title = episode_descr["movie_title"]
        episode_db.descr = episode_descr["descr_html"]
        episode_db.sub_json = subs
        episode_db.season = season_db
        episode_db.save()
    except Episode_db.DoesNotExist as e:
        logger.error(e) 
        try:
            episode_db = Episode_db(movie_title=episode_descr["movie_title"], movie_url=video_url, name=main_file_name, descr=episode_descr["descr_html"], abs_path=out_path, sub_json=subs, season=season_db, unique_id=uuid.uuid4().hex)
            episode_db.save()
        except django.db.utils.IntegrityError as e:
            logger.error(e)
            
    logger.info(episode_db.getDict())
    
    
def store_movie(main_path, name, main_moive_path, out_path, img_path, vtt_m3u8_subPath):
    main_file_name = name.split(".")
    main_file_name = ''.join(main_file_name[0:len(main_file_name) - 1])
    subs = json.dumps(extract_correct_subs(main_path, main_moive_path, vtt_m3u8_subPath))
    logger.info("extract_correct_subs movie " + str(subs))
    video_url = "/media/" + os.path.relpath(out_path, start=main_path).replace("\\", "/")
    parent_folder_path = Path(main_moive_path).resolve().parent
    try:
        category_db = Category_db.objects.get(category_path=parent_folder_path)
        category_db.category_name = os.path.basename(parent_folder_path)
        category_db.save()
    except Category_db.DoesNotExist as e:
        logger.error(e) 
        try:
            category_db = Category_db(category_path=parent_folder_path, category_name=os.path.basename(parent_folder_path))
            category_db.save()
        except django.db.utils.IntegrityError as e:
            logger.error(e)
    
    logger.info(category_db.getDict())
       
    logger.info("path_walker : " + str(main_file_name))
    desc_path = os.path.join(main_moive_path, "descr.json")
    if not os.path.isfile(desc_path) or FORCE_RETRIEVE_IMDB:
        desc_data = create_description_movie(desc_path, main_file_name)   
    else:
        desc_file = open(desc_path, "r") 
        desc_data = json.load(desc_file)
    descr_html = desc_data["descr_html"]
    movie_title = desc_data["movie_title"]
    try:
        movie_db = Movie_db.objects.get(abs_path=out_path)
        movie_db.movie_title = movie_title
        movie_db.name = main_file_name
        movie_db.img_url = img_path
        movie_db.movie_url = video_url
        movie_db.sub_json = json.dumps(subs)
        movie_db.descr = descr_html
        movie_db.category = category_db
        movie_db.save()
    except Movie_db.DoesNotExist as e:
        logger.error(e) 
        try:
            movie_db = Movie_db(movie_title=movie_title, name=main_file_name, abs_path=out_path, img_url=img_path, movie_url=video_url, sub_json=subs, unique_id=uuid.uuid4().hex, descr=descr_html, category=category_db)
            movie_db.save()
        except Exception as e:
            logger.error(str(e))
    
    logger.info(movie_db.getDescHTML())


def extract_correct_subs(main_path, main_moive_path, vtt_m3u8_subPath):
    subs_path = os.path.join(main_moive_path, "Subs")
    subs = []
    if not os.path.isdir(subs_path):
        return []
    old_subs_path = os.path.join(subs_path, "old_subs")
    try:
        os.mkdir(old_subs_path)
    except FileExistsError:
        pass
    if(os.path.isdir(subs_path)):
        for sub in os.listdir(subs_path):
            sub_path = os.path.join(subs_path, sub)
            if(os.path.isfile(sub_path)):
                if(sub_path.endswith(".srt")):
                    try:
                        webvtt_sub = webvtt.from_srt(sub_path)
                        webvtt_sub.save()
                    except Exception as e:
                        logger.error(str(e))
                if(not sub_path.endswith(".vtt")):
                    os.rename(sub_path, os.path.join(old_subs_path, sub))  
    
    subs = list(map(lambda x: os.path.relpath(os.path.join(subs_path, x), start=main_path).replace("\\", "/"), os.listdir(subs_path)))
    if vtt_m3u8_subPath != None:
        subs.append(os.path.relpath(os.path.join(subs_path, vtt_m3u8_subPath), start=main_path))
    subs = list(map(lambda sub_url:"/media/" + str(sub_url), filter(lambda sub:"vtt" in sub, subs)))
    return subs


def create_description_movie(desc_path, main_file_name):
    global ia
    if ia == None:
        logger.info("path_walker create_description_movie creating cinemagoer instance")
        ia = imdb.Cinemagoer()
    descr = []
    movie_title = ""
    try:
        if main_file_name in imdb_cache["movie"].keys():
            movie_imdb = imdb_cache["movie"][main_file_name]
        else:
            movie_imdb = ia.search_movie(main_file_name)
            logger.info("path_walker storing in imdb cache movie " + str(main_file_name))
            imdb_cache["movie"][main_file_name] = movie_imdb 
        if(len(movie_imdb) > 0):
            if str(movie_imdb[0].movieID) in imdb_cache_id["movie"].keys():
                mv = imdb_cache_id["movie"][str(movie_imdb[0].movieID)]
            else:
                mv = ia.get_movie(movie_imdb[0].movieID)
                logger.info("path_walker storing in imdb id cache movie id " + str(movie_imdb[0].movieID))
                imdb_cache_id["movie"][str(movie_imdb[0].movieID)] = mv
            if "title" in movie_imdb[0].keys():
                movie_title = movie_imdb[0]["title"]
            if "plot" in mv.keys():
                descr = mv["plot"].replace("<br/>","")
            elif "synopsis" in mv.keys():
                descr = mv["synopsis"].replace("<br/>","")
            elif "plot outline" in mv.keys():
                descr = mv["plot outline"].replace("<br/>","")
    except Exception as e:
        logger.error(str(e))
    descr_html = descr.replace("\n","<br/>") + "<br/>"
    descr_data = {"descr_html":descr_html, "movie_title":movie_title, "search":main_file_name}
    
    desc_file = open(desc_path, "w")
    
    json.dump(descr_data, desc_file)
    
    return descr_data

 
def create_description_episode(desc_path, show, seasons, episodes):
    global ia
    if ia == None:
        logger.info("path_walker create_description_episode creating cinemagoer instance")
        ia = imdb.Cinemagoer()
    movie_title = ""
    descr_html = ""
    try:
        if show in imdb_cache["show"].keys():
            movie_imdb = imdb_cache["show"][show]
        else:
            movie_imdb = ia.search_movie(show)
            logger.info("path_walker storing in imdb cache show " + str(show))
            imdb_cache["show"][show] = movie_imdb 
        if(len(movie_imdb) > 0):
            try:
                if str(movie_imdb[0].movieID) in imdb_cache_id["show"].keys():
                    mv = imdb_cache_id["show"][str(movie_imdb[0].movieID)]
                else:
                    mv = ia.get_movie(movie_imdb[0].movieID)
                    logger.info("path_walker storing in imdb id cache show id " + str(movie_imdb[0].movieID))
                    imdb_cache_id["show"][str(movie_imdb[0].movieID)] = mv
                ia.update(mv, 'episodes')
                for season in seasons:
                    for episode in episodes:
                        try:
                            if 'episodes' in mv.keys() and len(mv['episodes']) > int(season) and len(mv['episodes'][int(season)]) > int(episode):
                                ep = mv['episodes'][int(season)][int(episode)]
                                if "title" in ep.keys():
                                    movie_title += (str(ep["title"]).replace("<br/>","") + " <br/>")
                                if "plot" in ep.keys():
                                    descr_html += (str(ep["plot"]).replace("<br/>","") + " <br/>")
                                elif "synopsis" in ep.keys():
                                    descr_html += (str(ep["synopsis"]).replace("<br/>","") + " <br/>")
                                elif "plot outline" in ep.keys():
                                    descr_html += (str(ep["plot outline"]).replace("<br/>","") + " <br/>")
                        except Exception as e:
                            logger.error("create_description_episode " + str(e))
            except Exception as e:
                logger.error("create_description_episode " + str(e))
    except Exception as e:
        logger.error("create_description_episode " + str(e))
    descr_data = {"descr_html":descr_html, "movie_title":movie_title, "search":show + " " + str(seasons) + " " + str(episodes)}
    
    desc_file = open(desc_path, "w")
    
    json.dump(descr_data, desc_file)
    logger.info(str(descr_data))
    return descr_data 

    
def parse_media_dir():
    return parse_dir(os.path.join(BASE_DIR, 'media'))


if __name__ == "__main__":
    out = parse_media_dir()
    print(out)
