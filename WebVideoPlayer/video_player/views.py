from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
import logging

# Get an instance of a logger
logger = logging.getLogger("django")
#import video_player_utils
# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

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
    logger.info("redirect_internal"+str(response['X-Accel-Redirect']))
    return response
    """if request.user.is_authenticated:
        response = HttpResponse()
        response['X-Accel-Redirect'] = '/media-internal/' + path
        return response
    else:
        raise PermissionDenied()"""