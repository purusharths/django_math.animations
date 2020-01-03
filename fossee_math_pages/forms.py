from django import forms
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import UserDetails, Internship, Intern

INTERN_STATUS = (
    ("ACTIVE", "ACTIVE"),
    ("INACTIVE", "INACTIVE"),
)

STATUS = (
    ("ACTIVE", "ACTIVE"),
    ("INACTIVE", "INACTIVE"),
    ("COMPLETED", "COMPLETED"),
)

DATA_STATUS = (
    ("ACCEPTED", "ACCEPTED"),
    ("REJECTED", "REJECTED"),
    ("WAITING", "WAITING"),
    ("UNDER REVIEW", "UNDER REVIEW"),
)


class AddUserForm1(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class AddUserForm2(ModelForm):
    class Meta:
        model = UserDetails
        fields = ['user_phone', 'user_role']


class AddInternship(ModelForm):
    class Meta:
        model = Internship
        fields = ['internship_topic', 'internship_thumbnail', 'internship_status']


class ManageInternship(ModelForm):
    class Meta:
        model = Internship
        fields = ['internship_status']

class ManageIntern(ModelForm):
    class Meta:
        model = UserDetails
        fields = ['user_status']

class AddIntern(ModelForm):
    class Meta:
        model = Intern
        fields = '__all__'


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

# class add_data(forms.ModelForm):
#     text = RichTextUploadingField()

#     class Meta:
#         model = data
#         fields = ('subtopic', 'text',)


# # Edit data

# class edit_data(forms.ModelForm):
#     text = RichTextUploadingField()

#     class Meta:
#         model = data
#         fields = ('text',)

# class AddUserForm(forms.ModelForm):
#     firstname = forms.CharField(max_length=20)
#     lastname = forms.CharField(max_length=20)

#     class Meta:
#         model = AddUser
#         labels = {
#             "name" : "Username"
#         }
#         fields = ('firstname', 'lastname', 'name', 'email', 'topic', 'phone', 'role',)


# class DeleteUserForm(forms.ModelForm):
#     class Meta:
#         model = AddUser
#         fields = ('name', 'email',)
