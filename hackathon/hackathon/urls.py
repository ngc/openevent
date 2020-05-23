"""hackathon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include, re_path
from django.conf import settings
from users import views as users_views
from django.conf.urls.static import static
from django.conf.urls import url

app_name = 'administration'
urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('register/', users_views.register, name='register'),
    url(r'^user/', include('users.urls')),
    re_path(r'^team/(?P<teamid>[\w\s]+)/$', users_views.get_team, name="team"), 
    re_path(r'^submission/(?P<username>[a-zA-Z0-9]+)/$', users_views.get_submission_page, name="user_submission"), 
    path('mysubmission/', users_views.view_my_submission, name='mysubmission'),
    path('allsubmissions/', users_views.view_all_submissions, name='allsubmissions'),
  #  path('voting/', users_views.view_all_submissions, name='allsubmissions'),
    path('profile/', users_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='users/login.html')),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='users/logout.html')),
   path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('', include('blog.urls'), name='blog-home'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
