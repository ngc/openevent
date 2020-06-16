from django.shortcuts import render
from .models import BlogPost, InformationPost
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from blog import views as blog_views
from django.http import HttpResponse
from users.models import MasterControl
from django import template

# Create your views here.
@login_required
def home(request):
    context = {
        'posts': BlogPost.objects.all().order_by('-date'),
        'master': MasterControl.objects.get(identifier="MASTER")
    }
    return render(request, 'blog/home.html', context)

def info(request):
    context = {
        'posts': InformationPost.objects.all().order_by('-id'),
        'master': MasterControl.objects.get(identifier="MASTER")
    }
    return render(request, 'blog/info.html', context)