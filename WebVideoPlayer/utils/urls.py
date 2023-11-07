from django.urls import path

from . import views


urlpatterns = [
    path('list_dir', views.list_dir, name='list_dir'),
    path('list_items', views.list_items, name='list_items'),
    path('description', views.description, name='description'),
    path('scan_video_db', views.rescan_db, name='scan_video_db'),
    path('scan_db_dir', views.scan_db_dir, name='scan_db_dir'),
    path('list_media_dir', views.list_media_dir, name='list_media_dir'),
    path('edit_description', views.editDescriptionText,name="edit_description"),
]