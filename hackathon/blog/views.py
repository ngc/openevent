from django.shortcuts import render
from .models import BlogPost

posts = [

    {
        'author': 'Nathan',
        'title': 'Test 1',
        'content': 'LOLOLOLOOLOLOL',
        'date': 'Now' 
    },

    {
        'author': 'Not Nathan',
        'title': 'Test 2',
        'content': 'Not LOLOLOLOOLOLOL',
        'date': 'Not Now' 
    }

]


# Create your views here.
def home(request):
    context = {
        'posts': BlogPost.objects.all()
    }
    return render(request, 'blog/home.html', context)