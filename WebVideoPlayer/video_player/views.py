from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
import logging
import json
import os
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from utils.models import Movie_db,Episode_db, Season_db
from django.core.exceptions import ObjectDoesNotExist
# Get an instance of a logger
logger = logging.getLogger("django")
#import video_player_utils
# Create your views here.
def video(request):
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
        type=request.GET.get("type")
        logger.info("uuid "+str(uuid))
        play_src=""
        subs=[]
        try:
            if type=="movie":
                mv_db=Movie_db.objects.get(unique_id=uuid)
                play_src=mv_db.movie_url
                subs=json.loads(mv_db.sub_json)
                subs=[(sub,os.path.basename(sub)) for sub in subs]
                movie_name=mv_db.name
                return render(request,"main.html",{"movie_name":movie_name,"type":type,"play_src":play_src,"username":username,"subs":subs})
            elif type=="episode":
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
                subs=json.loads(ep_db.sub_json)
                subs=[(sub,os.path.basename(sub)) for sub in subs]
                season_name=str(ep_db.season.name)
                season_url="/entry_point?type=season&uuid="+str(ep_db.season.unique_id)
                episode_name=ep_db.name
                show_name=ep_db.season.show.name
                return render(request,"main.html",{"prv_ep_name":prv_ep_name,"prv_ep_uuid":prv_ep_uuid,"nxt_ep_name":nxt_ep_name,"nxt_ep_uuid":nxt_ep_uuid,"type":type,"play_src":play_src,"username":username,"subs":subs,"show_name":show_name,"episode_name":episode_name,"season_name":season_name,"season_url":season_url})
            else:
                play_src=""
                subs=[]
        except ObjectDoesNotExist:
            pass
        return render(request,"main.html",{"type":type,"play_src":play_src,"username":username,"subs":subs})
    #return HttpResponse("Hello, world. You're at the polls index.")

def index(request):
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
        type=None
        try:
            type=request.GET.get("type")
        except KeyError:
            return HttpResponseRedirect("/entry_point?type=movie")
        uuid=None
        try:
            uuid=request.GET.get("uuid")
        except KeyError:
            pass
        if type=="movie" or type=="show":
            return render(request,"main.html",{"play_src":request.GET.get("play"),"username":username,"type":type})
        elif type=="season" and uuid != None:
            return render(request,"main.html",{"username":username,"type":type,"uuid":uuid})
        else : 
            return HttpResponseRedirect("/entry_point?type=movie")

def bday(request):
    return HttpResponse("Happy B-Day !!")

def file_render(request):
    #print(request)
    return render(request,"file.html")

def file_render_html5(request):
    #print(request)
    return render(request,"file_html5.html")

def static_redirect_internal(request,path):
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
    curr_season=ep.season
    season_eps=Episode_db.objects.all().filter(season=curr_season.pk)
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
    show_seasons=Season_db.objects.all().filter(show=curr_show.pk)
    prev_season=None
    curr_season_ind=None
    for season in show_seasons:
        if season.abs_path==curr_season.abs_path:
            curr_season_ind=prev_season
            break
        prev_season=season
    
    if curr_season_ind==None:
        return None
    
    season_eps=Episode_db.objects.all().filter(season=curr_season_ind.pk)
    for episode in season_eps:
        if episode.abs_path==ep.abs_path:
            return curr_episode_ind
    
    return None
    
def next_ep(ep):
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
    for episode in season_eps:
        if episode.abs_path==ep.abs_path:
            return curr_episode_ind
    
    return None