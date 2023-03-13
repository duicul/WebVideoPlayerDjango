"""WebVideoPlayer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

import utils
import video_player

urlpatterns = [
    path('utils/', include('utils.urls')),
    path('video_player/', include('video_player.urls')),
    #path('admin/', admin.site.urls),
    path('login', utils.views.login,name="login"),
    path('logout',utils.views.logout,name="logout"),
    path('register',utils.views.register,name="register"),
    path('list_users',utils.views.list_users,name="list_users"),
    path('entry_point', video_player.views.index,name="entry_point"),
    path('upload_file', utils.views.upload_file,name="upload_file"),
    path('file_upload_form', utils.views.file_upload_form,name="file_upload_form"),
    path('file_upload_split', utils.views.file_upload_split,name="file_upload_split"),
]
if(not settings.DEBUG):
    urlpatterns.append(path('media/<path:path>', video_player.views.redirect_internal,name="redirect_internal"))
    #urlpatterns.append(path('static/<path:path>', video_player.views.static_redirect_internal,name="redirect_static"))
if settings.DEBUG:
    urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    #print(urlpatterns)"""