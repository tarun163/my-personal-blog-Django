from django.forms import ModelForm
from django.contrib.auth.forms import User

from django.contrib.auth.forms import UserCreationForm 
from django import forms
from .models import Comment


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name','email','body')        