from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    users = models.ManyToManyField(User)
    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.CharField(max_length=100, blank=True, default='', null=True)
    team = models.OneToOneField(Team, on_delete=models.CASCADE, blank=True, null=True)
    bio = models.TextField(blank=False, default='', null=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, created, instance, **kwargs):
    if created:
        instance.profile.save()