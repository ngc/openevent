from django.shortcuts import render, redirect
from . forms import UserRegisterForm, ProfileUpdateForm, SubmissionUpdateForm, TeamUpdateForm, VoteForm
from .models import Profile, Team, Submission, Vote, MasterControl
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from blog import views as blog_views
from django.http import HttpResponse
from random import shuffle
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.http import require_http_methods
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from django.contrib.auth.forms import PasswordChangeForm

def register(request):
    m = MasterControl.objects.get(identifier="MASTER")
    if request.method == 'POST' and m.allowing_new_users:
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account successfully created for {username}.')
            return redirect('/')
    else:
        form = UserRegisterForm()
    form = UserRegisterForm()
    if(m.allowing_new_users == False):
        messages.warning(request, f'Not accepting new users.')
    else:
        messages.warning(request, f'Account creation failed.')
    return render(request, 'users/register.html', {'form': form})


class ViewSubmissions(ListView):
    def dispatch(self, request, *args, **kwargs):
        m = MasterControl.objects.get(identifier="MASTER")
        if (m.allowing_viewing_submissions == False):
            return render(request, "users/notallowed.html", {'message': "Hold on! All submissions will be public at 6:00 PM on June 7th"})
        return super(ViewSubmissions, self).dispatch(request, *args, **kwargs)

    model = Submission
    queryset = Submission.objects.all().exclude(actualSubmission=False)
    template_name = "users/grading.html"
    context_object_name = "posts"
    ordering = ['-Score']
    paginate_by = 5


@login_required
def get_submission_page(request, username):
    m = MasterControl.objects.get(identifier="MASTER")
    if(request.user.is_superuser != True):
        if(m.allowing_viewing_submissions == False):
            return render(request, "users/notallowed.html", {'message': "Hold on! All submissions will be public at 6:00 PM on June 7th"})

    return render(request, 'users/mysubmission.html', {'post': Submission.objects.get(author=User.objects.get(username=username))})

@login_required
def view_my_submission(request):
    m = MasterControl.objects.get(identifier="MASTER")
    if(m.allow_submissions == False):
        return render(request, "users/notallowed.html", {'message': "Submissions are not allowed at this time."})

    if request.method == 'POST':
        p_form = SubmissionUpdateForm(request.POST, instance=Submission.objects.get(author=request.user))
        if p_form.is_valid():
            p_form.save()
            messages.success(request, f'Update successful.')
            return redirect('../mysubmission')
        else:
            messages.warning(request, f'Submission not allowed')
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

def get_team(request, teamid):
    teamobject = Team.objects.get(id=teamid)
    if(teamobject.users.all().count() == 1):
        return redirect("../../../../../user/" + str(teamobject.users.all()[0].username))
    if request.method == 'POST':
        p_form = TeamUpdateForm(request.POST, instance=teamobject)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, f'Update successful.')
            return redirect('../../team/' + str(teamobject.id) + "/")
    else:
        p_form = TeamUpdateForm(instance=teamobject)

    if(teamobject == request.user.profile.team):
        return render(request, 'users/team.html', {'team': teamobject, 'p_form': p_form})
    else:
        return render(request, 'users/team.html', {'team': teamobject})

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
    'profile': Profile.objects.get(user=User.objects.get(pk=request.user.id)),
    'page_title': request.user.username
    }
    return render(request, 'users/profile.html', context)

@login_required
def voting(request):
    m = MasterControl.objects.get(identifier="MASTER")
    if(m.allow_voting == False):
        return render(request, "users/notallowed.html", {'message': "Hold on! Voting will be allowed at 6:00 PM on June 7th"})

    if(request.user.profile.hasVoted):
        return redirect('../allsubmissions/')
    
    if request.method == 'POST':
        p_form = VoteForm(request.POST, instance=Vote.objects.get(user=request.user))
        if p_form.is_valid():
                p_form.save()

                Vote.objects.get(user=User.objects.get(pk=request.user.id))
                o = Profile.objects.get(user=User.objects.get(pk=request.user.id))
                o.hasVoted = True
                o.save()
                
                vote = Vote.objects.get(user=User.objects.get(pk=request.user.id))
                for i in vote.CHOICES.all():
                   f = Submission.objects.get(id=i.id)
                   f.Score = f.Score + 1
                   f.save()
                    

                messages.success(request, f'Thank you for voting!')
                return redirect('../profile')
    else:
        p_form = VoteForm(instance=request.user.vote)

    context = {
    'p_form': p_form,
    'profile': Profile.objects.get(user=User.objects.get(pk=request.user.id))
    }

    return render(request, 'users/voting.html', context)

@login_required
def winners(request):
    m = MasterControl.objects.get(identifier="MASTER")
    if(request.user.is_superuser != True):
        if(m.allow_viewing_winners == False):
            return redirect('../allsubmissions/')

    context = {
    'posts': Submission.objects.all().exclude(actualSubmission=False).order_by('Score').reverse()
    }

    return render(request, 'users/winners.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            messages.success(request, 'Your password was successfully updated!')
            return redirect('../profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/profile.html', {
        'p_form': form,
        'profile': Profile.objects.get(user=User.objects.get(pk=request.user.id))
    })