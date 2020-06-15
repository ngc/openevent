from django.contrib import admin
from .models import BlogPost, InformationPost

# Register your models here.
admin.site.site_header = 'MississaugaHacks Admin Panel'

class BlogPost_display(admin.ModelAdmin):
    list_display = ('title', 'author', 'imagelink', 'date')
    

admin.site.register(BlogPost, BlogPost_display)
admin.site.register(InformationPost, BlogPost_display)