from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path

urlpatterns = [
    re_path(r'(?P<username>[a-zA-Z0-9]+)$', views.get_user_profile, name="user"), #User path with parameter
]
