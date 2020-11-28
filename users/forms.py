from django import forms
from django.forms import ModelMultipleChoiceField, ValidationError
from django.contrib.auth.models import User
from .models import Profile, Submission, Team, Vote
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    """Form for registering a new User"""

    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            "firstname": "Firstname",
            "lastname": "Lastname",
        }

class ProfileRegisterForm(forms.ModelForm):
    """Form for creating a new Profile for a User"""

    class Meta:
        model = Profile
        fields = ('school', 'teamleader_username')
        labels = {
            "teamleader_username": "Team Leader Username",
        }

    def clean_teamleader_username(self):
        before = self.cleaned_data['teamleader_username']
        if(before == None): return ""
        if(User.objects.get(username = before)):
            return before
        else:
            raise ValidationError("Specified Team Leader Not Found")
        return before

    def clean_school(self):
        before = self.cleaned_data['school'] 
        if(before == None): raise ValidationError("Can't be empty")
        if("secondary" in before.lower() or "school" in before.lower() or "s.s" in before.lower() or " ss" in before.lower()):
            raise ValidationError("Do not include 'Secondary School', Example: 'Glenforest' not 'Glenforest Secondary School'")
        return before.strip()

class ProfileUpdateForm(forms.ModelForm):
    """Form for updating a User's Profile"""

    class Meta:
        model = Profile
        fields = ('bio',)

class TeamUpdateForm(forms.ModelForm):
    """Form for updating a Team's information"""
    
    class Meta:
        model = Team
        fields = ('name',)

class SubmissionUpdateForm(forms.ModelForm):
    """Form for updating information on a User's submission"""

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
        "actualSubmission": "Make Public",
        }


class VoteForm(forms.ModelForm):
    """Form for getting a User's vote on a submission"""

    class Meta:
        model = Vote
        fields = ['CHOICES']

    def clean_CHOICES(self):
        before = self.cleaned_data['CHOICES'] 
        if len(before) != 3:
            raise ValidationError("Choose exactly 3 submissions")
        else:
            return before

    def __init__(self, *args, **kwargs):
        super(VoteForm, self).__init__(*args, **kwargs)
        self.fields['CHOICES'] = forms.ModelMultipleChoiceField(queryset=Submission.objects.all().exclude(actualSubmission=False).exclude(
        author=self.instance.user).exclude(team=self.instance.user.profile.team),
        widget=forms.CheckboxSelectMultiple())

