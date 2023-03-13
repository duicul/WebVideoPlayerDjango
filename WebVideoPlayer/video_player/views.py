import os

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView
import psutil

import json
import logging
from pathlib import Path
import traceback 
from utils.models import Movie_db, Episode_db, Season_db, Show_db, Category_db

# Get an instance of a logger
logger = logging.getLogger("django")
BASE_DIR = Path(__file__).resolve().parent.parent
#import video_player_utils
# Create your views here.
def video(request):
    logger.info("video_player.video "+str(request))
    if 'processID' in request.session.keys():
        proc = request.session["processID"]
        logger.info('Process ID : '+str(proc))
        if proc!=None :
            if psutil.pid_exists(proc):
                log_status_path = os.path.join(BASE_DIR, 'logs/log_file_status.log')
                log_status=[]
                if os.path.isfile(log_status_path):
                    f = open(log_status_path,"r")
                    log_status = f.readlines()
                    f.close()
                return render(request,"loading.html",{"log_status":log_status})
            else:
                del request.session["processID"]
                request.session.modified = True
    username=None
    try:
        username=request.session['username']
    except KeyError:
        username=None
    #print(username)
    if(username==None):
        return HttpResponseRedirect("/entry_point")
    else:
        uuid=request.GET.get("play")
        type_name=request.GET.get("type")
        logger.info("uuid "+str(uuid))
        play_src=""
        subs=[]
        try:
            if type_name=="movie":
                mv_db=Movie_db.objects.get(unique_id=uuid)
                play_src=mv_db.movie_url
                #logger.info("movie subs"+str(mv_db.sub_json))
                subs=json.loads(mv_db.sub_json)
                if(isinstance(subs, str)):
                    subs = subs.strip(']["').split(',')
                #logger.info("movie subs"+str(subs))
                subsaux=[]
                for sub in subs:
                    #logger.info("movie subs sub"+str(sub))
                    subsaux.append((sub,os.path.basename(sub)))
                subs=subsaux    
                #logger.info("movie subs"+str(subs))
                movie_name=mv_db.name
                descr = mv_db.descr
                resp = {"movie_name":movie_name,"type":type_name,"play_src":play_src,"username":username,"description":descr}
                if len(subs)>0:
                    resp["subs"] = subs
                return render(request,"main.html",resp)
            elif type_name=="episode":
                ep_db=Episode_db.objects.get(unique_id=uuid)
                prv_ep=previous_ep(ep_db)
                nxt_ep=next_ep(ep_db)
                prv_ep_name=None
                prv_ep_uuid=None
                nxt_ep_name=None
                nxt_ep_uuid=None
                if prv_ep != None:
                    prv_ep_name=prv_ep.name
                    prv_ep_uuid=prv_ep.unique_id
                if nxt_ep != None:
                    nxt_ep_name=nxt_ep.name
                    nxt_ep_uuid=nxt_ep.unique_id
                play_src=ep_db.movie_url
                logger.info("episode subs"+str(ep_db.sub_json))
                subs=json.loads(ep_db.sub_json)
                if(isinstance(subs, str)):
                    subs = subs.strip(']["').split(',')
                #logger.info("episode subs"+str(subs))
                subsaux=[]
                for sub in list(subs):
                    #logger.info("episode subs sub"+str(sub))
                    subsaux.append((sub,os.path.basename(sub)))
                subs=subsaux
                #subs=[(sub,os.path.basename(sub)) for sub in subs]
                #logger.info("episode subs"+str(subs))
                season_name=str(ep_db.season.name)
                season_id = str(ep_db.season.unique_id)
                season_url="/entry_point?type=season&uuid="+str(ep_db.season.unique_id)
                episode_name=ep_db.name
                show_name=ep_db.season.show.name
                descr = ep_db.descr
                episodes = []
                """try:
                    episodes=[episode.getDict() for episode in Episode_db.objects.filter(season=ep_db.season.pk).order_by('name')]
                except Exception as e:
                    logger.error(str(traceback.format_exc()))"""
                resp = {"prv_ep_name":prv_ep_name,"prv_ep_uuid":prv_ep_uuid,"nxt_ep_name":nxt_ep_name,"nxt_ep_uuid":nxt_ep_uuid,"type":type_name,"play_src":play_src,"username":username,"subs":subs,"show_name":show_name,"episode_name":episode_name,"season_name":season_name,"season_url":season_url,"season_id":season_id,"description":descr,"episodes":episodes}
                if len(subs)>0:
                    resp["subs"] = subs
                return render(request,"main.html",resp)
            else:
                play_src=""
                subs=[]
        except ObjectDoesNotExist:
            pass
        resp = {"type":type_name,"play_src":play_src,"username":username,"subs":subs,"description":""}
        if len(subs)>0:
            resp["subs"] = subs
        return render(request,"main.html",resp)
    #return HttpResponse("Hello, world. You're at the polls index.")

def index(request):
    logger.info("video_player.index "+str(request))
    global process
    if 'processID' in request.session.keys():
        proc = request.session["processID"]
        logger.info('Process ID : '+str(proc))
        if proc!=None :
            if psutil.pid_exists(proc):
                log_status_path = os.path.join(BASE_DIR, 'logs/log_file_status.log')
                log_status=[]
                if os.path.isfile(log_status_path):
                    f = open(log_status_path,"r")
                    log_status = f.readlines()
                    f.close()
                return render(request,"loading.html",{"log_status":log_status})
            else:
                del request.session["processID"]
                request.session.modified = True
    username=None
    login=None
    try:
        username=request.session['username']
    except KeyError:
        username=None
    try:
        login=request.GET.get("login")
    except KeyError:
        login=None
    #print(username)
    if(username==None):
        return render(request,"index.html",{"login":login})
    else:
        type_name=None
        try:
            type_name=request.GET.get("type")
        except KeyError:
            return HttpResponseRedirect("/entry_point?type=movie")
        category_name=None
        try:
            category_name=request.GET.get("category")
        except KeyError:
            category_name=None
        uuid=None
        try:
            uuid=request.GET.get("uuid")
        except KeyError:
            pass
        categ = []
        if type_name=="movie":
            for movie in Movie_db.objects.all().order_by('name'):
                if not movie.category in categ:
                    categ.append(movie.category)
        elif type_name=="show":
            for show in Show_db.objects.all().order_by('name'):
                if not show.category in categ:
                    categ.append(show.category)
        categ = sorted(categ,key=lambda c: c.category_name)
        categ = list(map(lambda categ : categ.getDict(),categ))
        if type_name=="movie" or type_name == "show":
            movie_list = []
            c=None
            if category_name != None:
                c = Category_db.objects.get(category_name=category_name)
                c=c.category_name
            return render(request,"main.html",{"play_src":request.GET.get("play"),"username":username,"type":type_name,"categ":categ,"category":c})
        elif type_name=="season" and uuid != None:
            season = Season_db.objects.get(unique_id=uuid)
            season_name = season.name
            return render(request,"main.html",{"username":username,"type":type_name,"uuid":uuid,"categ":categ,"season_name":season_name})
        else : 
            return HttpResponseRedirect("/entry_point?type=movie")

def bday(request):
    return HttpResponse("Happy B-Day !!")

def file_render(request):
    #print(request)
    return render(request,"file.html")

def file_render_html5(request):
    logger.info("video_player.file_render_html5 "+str(request))
    return render(request,"file_html5.html")

def static_redirect_internal(request,path):
    logger.info("video_player.static_redirect_internal "+str(request)+" "+str(path))
    #print(settings.DEBUG)
    username=None
    try:
        username=request.session['username']
    except KeyError:
        raise PermissionDenied()
    response = HttpResponse()
    response['X-Accel-Redirect'] = '/static-internal/' + path
    logger.info("redirect_internal media = "+str(response['X-Accel-Redirect']))
    return response

def redirect_internal(request,path):
    logger.info("video_player.redirect_internal "+str(request)+" "+str(path))
    username=None
    try:
        username=request.session['username']
    except KeyError:
        raise PermissionDenied()
    response = HttpResponse()
    response['X-Accel-Redirect'] = '/media-internal/' + path
    logger.info("redirect_internal static = "+str(response['X-Accel-Redirect']))
    return response

def previous_ep(ep):
    logger.info("video_player.previous_ep "+str(ep))
    curr_season=ep.season
    season_eps=Episode_db.objects.all().filter(season=curr_season.pk).order_by("-abs_path")
    prev_episode=None
    curr_episode_ind=None
    
    for episode in season_eps:
        if episode.abs_path==ep.abs_path:
            curr_episode_ind=prev_episode
            if prev_episode!=None:
                return curr_episode_ind
            break
        prev_episode=episode
    
    
    if curr_episode_ind == None and prev_episode!=None:
        return None
    
    curr_show=curr_season.show
    show_seasons=Season_db.objects.all().filter(show=curr_show.pk).order_by("-abs_path")
    prev_season=None
    curr_season_ind=None
    for season in show_seasons:
        if season.abs_path==curr_season.abs_path:
            curr_season_ind=prev_season
            break
        prev_season=season
    
    if curr_season_ind==None:
        return None
    
    season_eps=Episode_db.objects.all().filter(season=curr_season_ind.pk).order_by("-abs_path")
    if len(season_eps)==0:
        return None
    return season_eps[len(season_eps)-1]
    
def next_ep(ep):
    logger.info("video_player.next_ep "+str(ep))
    curr_season=ep.season
    season_eps=Episode_db.objects.all().filter(season=curr_season.pk).order_by("-abs_path")
    prev_episode=None
    curr_episode_ind=None
    
    for episode in season_eps:
        if episode.abs_path==ep.abs_path:
            curr_episode_ind=prev_episode
            if prev_episode!=None:
                return curr_episode_ind
            break
        prev_episode=episode
    
    
    if curr_episode_ind == None and prev_episode!=None:
        return None
    
    curr_show=curr_season.show
    show_seasons=Season_db.objects.all().filter(show=curr_show.pk).order_by("-abs_path")
    prev_season=None
    curr_season_ind=None
    for season in show_seasons:
        if season.abs_path==curr_season.abs_path:
            curr_season_ind=prev_season
            break
        prev_season=season
    
    if curr_season_ind==None:
        return None
    
    season_eps=Episode_db.objects.all().filter(season=curr_season_ind.pk).order_by("-abs_path")
    if len(season_eps)==0:
        return None
    return season_eps[len(season_eps)-1]