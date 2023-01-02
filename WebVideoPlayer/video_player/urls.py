from django.conf import settings
from django.urls import path

from . import views


urlpatterns = [
    path('', views.video, name='main_video'),
    path('bday', views.bday, name='happy_bday'),
    path('file',views.file_render,name="file_render"),
    path('file_html5',views.file_render_html5,name="file_render_html5")
]

