from django.shortcuts import render
from django.http import HttpResponse
#import video_player_utils
# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def bday(request):
    return HttpResponse("Happy B-Day !!")

def file_render(request):
    print(request)
    return render(request,"file.html")