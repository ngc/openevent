from django.shortcuts import render, redirect
from . forms import UserRegisterForm as UserCreationForm
from django.contrib import messages
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
