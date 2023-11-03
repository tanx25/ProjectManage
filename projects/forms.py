from django import forms
from .models import Project, Step, CustomUser
from django.contrib.auth.forms import UserCreationForm

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']

class StepForm(forms.ModelForm):
    class Meta:
        model = Step
        fields = ['name', 'status']



class CustomUserCreationForm(UserCreationForm):
    gender = forms.ChoiceField(choices=CustomUser.GENDER_CHOICES)
    condition = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))
    notes = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'address', 'gender', 'study_id', 'condition', 'notes')

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'address', 'gender', 'study_id', 'condition', 'notes']




