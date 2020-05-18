from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    users = models.ManyToManyField(User)
    def __str__(self):
        return self.name

class Submission(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    
    Main_Link = models.CharField(max_length=100, default='https://www.google.com/',)
    label_Main_Link = models.CharField(max_length=26, default='Main',)
    
    Link2 = models.CharField(max_length=100, default='', blank=True)
    label_Link2 = models.CharField(max_length=26, default='Link 2', blank=True)

    Link3 = models.CharField(max_length=100, default='', blank=True)
    label_Link3 = models.CharField(max_length=26, default='Link 3', blank=True)

    Link4 = models.CharField(max_length=100, default='', blank=True)
    label_Link4 = models.CharField(max_length=26, default='Link 4', blank=True)
    
    imagelink = models.CharField(max_length=100, default='', blank=True)
    actualSubmission = models.BooleanField(default=False)
    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.CharField(max_length=100, blank=True, default='', null=True)
    team = models.ManyToManyField(Team, blank=True)
    bio = models.TextField(blank=False, default='', null=True)
    submission = models.OneToOneField(Submission, blank=True, null=True, on_delete=models.CASCADE)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, created, instance, **kwargs):
    if created:
        instance.profile.save()