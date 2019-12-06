from django import forms
from django.utils import timezone
from .models import (profile, data, )
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import os
from django.core.exceptions import ValidationError
from froala_editor.widgets import FroalaEditor
from .models import AddUser

position_choices = (
    ("intern", "intern"),
    ("staff", "staff"),
)


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=32, widget=forms.TextInput())
    password = forms.CharField(max_length=32, widget=forms.PasswordInput())

    def clean(self):
        super(UserLoginForm, self).clean()
        try:
            uname, pwd = self.cleaned_data["username"], \
                          self.cleaned_data["password"]
            user = authenticate(username=uname, password=pwd)
        except Exception:
            raise forms.ValidationError \
                ("Username and/or Password is not entered")
        if not user:
            raise forms.ValidationError("Invalid username/password")
        return user



class add_data(forms.ModelForm):
    subtopic=forms.CharField
    content = forms.CharField(widget=FroalaEditor)

    class Meta:
        model = data
        fields = ('subtopic', 'content')

class AddUserForm(forms.ModelForm):
    class Meta:  
        model = AddUser  
        fields = ('name', 'email', 'topic', 'phone', 'role',) 

class DeleteUserForm(forms.ModelForm):
    class Meta:  
        model = AddUser  
        fields = ('name', 'email',) 