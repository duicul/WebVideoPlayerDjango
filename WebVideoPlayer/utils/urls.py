from django.urls import path

from . import views

urlpatterns = [
    path('list_dir', views.list_dir, name='list_dir'),
    path('list_video_files', views.list_video_files, name='list_video_files'),
]