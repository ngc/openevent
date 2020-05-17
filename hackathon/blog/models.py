from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    imagelink = models.CharField(max_length=100, default='', blank=True)
    

    def __str__(self):
        return self.title
    imagelink.short_description = 'To host images, upload them to Imgur at https://imgur.com/'