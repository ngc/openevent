from django import forms
from django.contrib.auth.models import User
from .models import Profile, Submission
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio',)

class SubmissionUpdateForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ('title', 'content', 'imagelink', 'actualSubmission')