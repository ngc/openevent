from django import forms
from django.forms import ModelMultipleChoiceField, ValidationError
from django.contrib.auth.models import User
from .models import Profile, Submission, Team, Vote
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

class VoteForm(forms.ModelForm):

    choices = forms.ModelMultipleChoiceField(queryset=Submission.objects.filter(actualSubmission=False), widget=forms.CheckboxSelectMultiple())
    class Meta:
        model = Vote
        fields = ('choices',)

#    def __init__(self, *args, **kwargs):
 #       super().__init__(*args, **kwargs)
  #      self.fields['ch'].widget=forms.CheckboxSelectMultiple()

    def clean_choices(self):
        if len(self.cleaned_data['choices']) == 3:
            return self.cleaned_data['choices']
        else:
            raise ValidationError("Choose exactly 3 submissions")


# #
#class VoteForm(forms.Form):
#    class Meta:
#        model = Vote
#        
#
#        

#  