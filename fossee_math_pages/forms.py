from django import forms
from django.utils import timezone
from .models import (profile, )
from string import punctuation, digits
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

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
            u_name, pwd = self.cleaned_data["username"], \
                          self.cleaned_data["password"]
            user = authenticate(username=u_name, password=pwd)
        except Exception:
            raise forms.ValidationError \
                ("Username and/or Password is not entered")
        if not user:
            raise forms.ValidationError("Invalid username/password")
        return user

def validate_file_extension(value):
    if not value.name.endswith('.csv'):
        raise forms.ValidationError("Only CSV file is accepted")

class AddForm(forms.Form):
    docfile = forms.FileField(label='Select a file',validators=[validate_file_extension])
    
    