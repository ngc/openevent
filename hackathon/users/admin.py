from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.
from users.models import Profile, Team

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]

class Team_display(admin.ModelAdmin):
    list_display = ['name']

admin.site.unregister(User)
admin.site.register(Team, Team_display)
admin.site.register(User, UserAdmin)