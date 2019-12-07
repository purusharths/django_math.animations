from ckeditor.fields import RichTextFormField
from django import forms
from django.contrib.auth import authenticate
from .models import AddUser, data

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
    content=RichTextFormField()
    class Meta:
        model = data
        fields=('subtopic','content',)


class AddUserForm(forms.ModelForm):
    class Meta:
        model = AddUser
        fields = ('name', 'email', 'topic', 'phone', 'role',)

