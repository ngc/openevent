from django.shortcuts import render
from blog.models import BlogPost
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from blog import views as blog_views
from django.http import HttpResponse
from users.models import MasterControl
from django import template
from time import time
import datetime
import pytz
import math

register = template.Library() #Declare register for decorator 

@register.simple_tag(name='get_event_name')
def get_event_name():
    return MasterControl.objects.get(identifier="MASTER").event_name

@register.simple_tag(name='get_time_until')
def get_time_until(type):
    #Example Date: "January 1, 2030 00:00:00"
    d = datetime.datetime.strptime(MasterControl.objects.get(identifier="MASTER").timer_date, '%B %d, %Y %H:%M:%S')

    distance = (d - datetime.datetime.now()).total_seconds() * 1000
    
    if(type == "D"): return math.floor(distance / (1000 * 60 * 60 * 24))
    if(type == "H"): return math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
    if(type == "M"): return math.floor((distance % (1000 * 60 * 60)) / (1000 * 60))
    if(type == "S"): return math.floor((distance % (1000 * 60)) / 1000)
    if(type == "DATE"): return MasterControl.objects.get(identifier="MASTER").timer_date