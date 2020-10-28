from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('bday', views.bday, name='happy_bday'),
    path('file',views.file_render,name="file_render"),
    path('file_html5',views.file_render_html5,name="file_render_html5")
]
if(not settings.DEBUG):
    urlpatterns.append(path('media/<path:path>', views.redirect_internal,name="redirect_internal"))
