from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import random
import string

def GenRandom(length):
    letters = string.digits + string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

def GenRandomUser(length):
    letters = string.digits
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
    team = models.ForeignKey(Team, on_delete = models.CASCADE, blank=True, null=True)
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
    teamleader_username = models.CharField(max_length=100, blank=True, default='', null=True)

class Vote(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    CHOICES = models.ManyToManyField(Submission, blank=True)

class MasterControl(models.Model):
    allowing_new_users = models.BooleanField(default=True)
    allowing_viewing_submissions = models.BooleanField(default=False)
    allow_submissions = models.BooleanField(default=True)
    allow_viewing_winners = models.BooleanField(default=False)
    allow_voting = models.BooleanField(default=False)
    allow_viewing_platform = models.BooleanField(default=False)
    platform_not_allowed_redirect = models.CharField(default="https://www.google.com/", max_length=300)
    submissions_not_allowed_message = models.CharField(default="Hold on! Submissions will be allowed at 6:00 PM", max_length=300)
    viewing_submissions_not_allowed_message = models.CharField(default="Hold on! Viewing Submissions will be allowed at 6:00 PM", max_length=300)
    voting_not_allowed_message = models.CharField(default="Hold on! Voting will be allowed at 6:00 PM", max_length=300)
    winners_not_allowed_message = models.CharField(default="Hold on! Winners will be allowed at 6:00 PM", max_length=300)
    timer_date = models.CharField(max_length=100, default="January 1, 2030 00:00:00")
    timer_message = models.CharField(max_length=100, default="Event starts on January 1st, 2030!")
    youtube_embed_code = models.CharField(max_length=100, default="S7SLep244ss")
    event_name = models.CharField(max_length=20, default="MississaugaHacks2020")
    identifier = models.TextField(blank=False, default='MASTER', null=True)
    def __str__(self):
        return self.identifier

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    global SubmissionIDCounter
    if created:
        Profile.objects.create(user=instance)
        Submission.objects.create(author=instance)
        Vote.objects.create(user=instance)
        #Editing default data with dynamic details
        instance.profile.submission = instance.submission
        instance.submission.title = instance.get_short_name() + "'s Submission " + GenRandom(9) 
        instance.submission.imagelink = "https://techcrunch.com/wp-content/uploads/2015/04/codecode.jpg" 

@receiver(post_save, sender=User)
def save_user_profile(sender, created, instance, **kwargs):
    if created:
        instance.username = instance.first_name.strip() + str(GenRandomUser(3))
        instance.save()
        instance.profile.save()
        instance.submission.save()
        instance.vote.save()