from django.shortcuts import render
from .models import BlogPost

# Create your views here.
def home(request):
    context = {
        'posts': BlogPost.objects.all()
    }
    return render(request, 'blog/home.html', context)