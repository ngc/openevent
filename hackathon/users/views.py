from django.shortcuts import render, redirect
from . forms import UserRegisterForm, ProfileUpdateForm, SubmissionUpdateForm, TeamUpdateForm
from .models import Profile, Team, Submission
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from blog import views as blog_views
from django.http import HttpResponse

allowing_new_users = True #Change this value if registration should be allowed or not 
                          #Mississauga Hacks should use false at the start of the event

def register(request):
    if request.method == 'POST' and allowing_new_users:
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account successfully created for {username}.')
            return redirect('/')
    else:
        form = UserRegisterForm()
    form = UserRegisterForm()
    if(allowing_new_users == False):
        messages.warning(request, f'Not accepting new users.')
    else:
        messages.warning(request, f'Account creation failed.')
    return render(request, 'users/register.html', {'form': form})

@login_required
def view_all_submissions(request):
    return render(request, 'users/grading.html', {'posts': Submission.objects.all()})

@login_required
def get_submission_page(request, username):
    return render(request, 'users/mysubmission.html', {'post': Submission.objects.get(author=User.objects.get(username=username))})

@login_required
def view_my_submission(request):
    if request.method == 'POST':
        p_form = SubmissionUpdateForm(request.POST, instance=Submission.objects.get(author=request.user))
        if p_form.is_valid():
            p_form.save()
            messages.success(request, f'Update successful.')
            return redirect('../mysubmission')
    else:
        p_form = SubmissionUpdateForm(instance=Submission.objects.get(author=request.user))

    context = {
    'form': p_form,
    'post': Submission.objects.get(author=request.user)
    }
    return render(request, 'users/mysubmission.html', context)

@login_required
def get_user_profile(request, username):
    p = Profile.objects.get(user=User.objects.get(username=username))
    if(request.user.username == username): return profile(request)
    return render(request, 'users/profile.html', {"profile": p})

def get_team(request, team):
    teamobject = Team.objects.get(name=team)
    if request.method == 'POST':
        p_form = TeamUpdateForm(request.POST, instance=teamobject)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, f'Update successful.')
            return redirect('../../team/' + teamobject.name + "/")
    else:
        p_form = TeamUpdateForm(request.POST, instance=teamobject)

    if(team == request.user.profile.team.name):
        return render(request, 'users/team.html', {'team': teamobject, 'p_form': p_form})
    else:
        return render(request, 'users/team.html', {'team': teamobject,})

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
    'profile': Profile.objects.get(user=User.objects.get(pk=request.user.id))
    }
    return render(request, 'users/profile.html', context)

