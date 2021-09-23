from .models import Profile,Project,Rate
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreateProfileForm(ModelForm):
  class Meta:
    model=Profile
    exclude =['user']

class UpdateProfileForm(ModelForm):
  class Meta:
    model=Profile
    exclude=['user']


class ProjectForm(ModelForm)
  class Meta:
    model=Project
    exclude=['profile', 'post_date',]

class RateForm(ModelForm):
  class Meta:
    model=Rate
    fields=['design','usability','content']
    

class CreateUserForm(UserCreationForm):
  class Meta:
    model=User
    fields=['username', 'email','password1','password2']