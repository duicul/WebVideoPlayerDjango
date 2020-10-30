from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
import logging
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from utils.models import Movie_db
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
    print(username)
    if(username==None):
        return HttpResponseRedirect("/")
    else:
        uuid=request.GET.get("play")
        logger.info("uuid "+str(uuid))
        play_src=""
        try:
            mv_db=Movie_db.objects.get(unique_id=uuid)
            play_src=mv_db.movie_url
        except ObjectDoesNotExist:
            pass
        return render(request,"main.html",{"play_src":play_src,"username":username})
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
    print(username)
    if(username==None):
        return render(request,"index.html",{"login":login})
    else:
        return render(request,"main.html",{"play_src":request.GET.get("play"),"username":username})
    
def bday(request):
    return HttpResponse("Happy B-Day !!")

def file_render(request):
    print(request)
    return render(request,"file.html")

def file_render_html5(request):
    print(request)
    return render(request,"file_html5.html")

def redirect_internal(request,path):
    print(settings.DEBUG)
    logger.info("debug = "+str(settings.DEBUG))
    response = HttpResponse()
    response['X-Accel-Redirect'] = '/media-internal/' + path
    logger.info("redirect_internal = "+str(response['X-Accel-Redirect']))
    return response
    """if request.user.is_authenticated:
        response = HttpResponse()
        response['X-Accel-Redirect'] = '/media-internal/' + path
        return response
    else:
        raise PermissionDenied()"""