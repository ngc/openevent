from django.shortcuts import render, redirect
from . forms import UserRegisterForm as UserCreationForm, ProfileUpdateForm
from .models import Profile
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from blog import views as blog_views

allowing_new_users = True #Change this value if registration should be allowed or not 
                          #Mississauga Hacks should use false at the start of the event

def register(request):
    if request.method == 'POST' and allowing_new_users:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account successfully created for {username}.')
            return redirect('/')
    else:
        form = UserCreationForm()
    form = UserCreationForm()
    if(allowing_new_users == False):
        messages.warning(request, f'Not accepting new users.')
    else:
        messages.warning(request, f'Account creation failed.')
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, f'Update successful.')
            return redirect('../profile')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
    'p_form': p_form,
    'profile': User.objects.get(pk=request.user.id)
    }
    return render(request, 'users/profile.html', context)

