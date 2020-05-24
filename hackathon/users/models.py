from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import random
import string


def GenRandom(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

class Team(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    users = models.ManyToManyField(User)
    def __str__(self):
        return self.name

class Submission(models.Model):
    title = models.CharField(max_length=100, default="Submission")
    content = models.TextField(default="Nothing has been written about this submission yet....")
    date = models.DateTimeField(auto_now=True)
    author = models.OneToOneField(User, on_delete = models.CASCADE)
    Main_Link = models.CharField(max_length=100, default='https://www.google.com/',)
    label_Main_Link = models.CharField(max_length=26, default='Main',)
    Link2 = models.CharField(max_length=100, default='', blank=True)
    label_Link2 = models.CharField(max_length=26, default='Link 2', blank=True)
    Link3 = models.CharField(max_length=100, default='', blank=True)
    label_Link3 = models.CharField(max_length=26, default='Link 3', blank=True)
    Link4 = models.CharField(max_length=100, default='', blank=True)
    label_Link4 = models.CharField(max_length=26, default='Link 4', blank=True)
    imagelink = models.CharField(max_length=100, default='', blank=True)
    Score = models.IntegerField(default=0)

    actualSubmission = models.BooleanField(default=False)
    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.CharField(max_length=100, blank=True, default='', null=True)
    team = models.ForeignKey(Team, blank=True, on_delete=models.CASCADE, null=True)
    bio = models.TextField(blank=False, default='Nothing has been written here yet...', null=True)
    submission = models.OneToOneField(Submission, blank=True, null=True, on_delete=models.CASCADE)
    hasVoted = models.BooleanField(default=False)

class Vote(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    CHOICES = models.ManyToManyField(Submission, blank=True)

class MasterControl(models.Model):
    allowing_new_users = models.BooleanField(default=True)
    allowing_viewing_submissions = models.BooleanField(default=False)
    allow_submissions = models.BooleanField(default=True)
    allow_viewing_winners = models.BooleanField(default=False)
    allow_voting = models.BooleanField(default=False)
    identifier = models.TextField(blank=False, default='MASTER', null=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    global SubmissionIDCounter
    if created:
        Profile.objects.create(user=instance)
        Submission.objects.create(author=instance)
        Vote.objects.create(user=instance)
        #Editing default data with dynamic details
        instance.profile.submission = instance.submission
        instance.submission.title = "Submission " + GenRandom(9) 

@receiver(post_save, sender=User)
def save_user_profile(sender, created, instance, **kwargs):
    if created:
        instance.profile.save()
        instance.submission.save()
        instance.vote.save()