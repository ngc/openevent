from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class BlogPost(models.Model):
    """
    Basic blog post model, supports images 
    """
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    imagelink = models.CharField(max_length=100, default='', blank=True)
    
    def __str__(self):
        return self.title

# Create your models here.
class InformationPost(models.Model):
    """
    Information Post, supports added HTML
    """
    title = models.CharField(max_length=100)
    HTML_content = models.TextField()
    content = models.TextField()
    date = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    imagelink = models.CharField(max_length=100, default='', blank=True)
    
    def __str__(self):
        return self.title