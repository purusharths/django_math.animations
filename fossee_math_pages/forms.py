from ckeditor.fields import RichTextFormField
from ckeditor_uploader.fields import RichTextUploadingField
from django import forms
from django.contrib.auth import authenticate
from .models import AddUser, data

position_choices = (
    ("intern", "intern"),
    ("staff", "staff"),
)
status_choices = (
    ("ACTIVE", "ACTIVE"),
    ("INACTIVE", "INACTIVE"),
    ("SUSPENDED", "SUSPENDED"),
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
    text = RichTextUploadingField()

    class Meta:
        model = data
        fields = ('subtopic', 'text',)


# Edit data

class edit_data(forms.ModelForm):
    text = RichTextUploadingField()

    class Meta:
        model = data
        fields = ('text',)

class AddUserForm(forms.ModelForm):
    firstname = forms.CharField(max_length=20)
    lastname = forms.CharField(max_length=20)

    class Meta:
        model = AddUser
        labels = {
            "name" : "Username"
        }
        fields = ('firstname', 'lastname', 'name', 'email', 'topic', 'phone', 'role',)


class DeleteUserForm(forms.ModelForm):
    class Meta:
        model = AddUser
        fields = ('name', 'email',)


