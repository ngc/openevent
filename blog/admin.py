from django.contrib import admin
from .models import BlogPost, InformationPost

# Register your models here.
admin.site.site_header = 'OpenEvent Admin Panel' #Sets internal title of admin page

class BlogPost_display(admin.ModelAdmin):
    list_display = ('title', 'author', 'imagelink', 'date') #Display blog post information in admin panel for easy identification and editing

admin.site.register(BlogPost, BlogPost_display)
admin.site.register(InformationPost, BlogPost_display)