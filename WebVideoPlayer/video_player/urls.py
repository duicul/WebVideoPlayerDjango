from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('bday', views.bday, name='happy_bday'),
    path('file',views.file_render,name="file_render")
]