from django.db import models

# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=100)