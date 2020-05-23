from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from users.models import Profile, Team, Submission, Vote

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class SubmissionInLine(admin.StackedInline):
    model = Submission
    can_delete = False

class VoteInLine(admin.StackedInline):
    model = Vote
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline, SubmissionInLine, VoteInLine]
    readonly_fields = ('id',)

class Team_display(admin.ModelAdmin):
    list_display = ['name']
    readonly_fields = ('id',)

admin.site.unregister(User)
admin.site.register(Team, Team_display)
admin.site.register(User, UserAdmin)
admin.site.register(Submission)