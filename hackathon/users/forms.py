from django import forms
from django.contrib.auth.models import User
from .models import Profile, Submission, Team
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

class TeamUpdateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name',)

class SubmissionUpdateForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ('title', 'content', 'imagelink', 'Main_Link', 'label_Main_Link', 'Link2', 'label_Link2', 'Link3', 'label_Link3', 'Link4', 'label_Link4', 'actualSubmission')
        labels = {
        "title": "Title", 
        "content": "Content",
        "imagelink": "Image Link",
        "Main_Link": "Main Link (Example https://www.google.com, not www.google.com)",
        "Link2": "Link 2 (Optional)",
        "Link3": "Link 3 (Optional)",
        "Link4": "Link 4 (Optional)",
        "label_Main_Link": "Label for Main Link",
        "label_Link2": "Label for Link 2",
        "label_Link3": "Label for Link 3",
        "label_Link4": "Label for Link 4",
        "actualSubmission": "Actual Submission",
        }