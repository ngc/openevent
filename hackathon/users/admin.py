from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from users.models import Profile, Team, Submission, Vote, ViewsMasterControlBoard

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

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'Score']

class ViewsMasterControlBoardAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.unregister(User)
admin.site.register(Team, Team_display)
admin.site.register(User, UserAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(ViewsMasterControlBoard, ViewsMasterControlBoardAdmin)