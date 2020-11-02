from django.urls import path

from . import views

urlpatterns = [
    path('list_dir', views.list_dir, name='list_dir'),
    path('list_video', views.list_video, name='list_video'),
    path('scan_video_db', views.rescan_db, name='scan_video_db'),
]