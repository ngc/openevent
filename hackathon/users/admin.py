from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from users.models import Profile, Team, Submission

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class SubmissionInLine(admin.StackedInline):
    model = Submission
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline, SubmissionInLine]

class Team_display(admin.ModelAdmin):
    list_display = ['name']

admin.site.unregister(User)
admin.site.register(Team, Team_display)
admin.site.register(User, UserAdmin)
admin.site.register(Submission)