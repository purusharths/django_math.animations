from django import forms
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import UserDetails, Internship, Intern, Topic, Subtopic, AssignedTopics,Data

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
        labels = {
            'user_id' : 'Intern Name',
            'internship_id' : 'Internship Name'
        }
        fields = ['user_id','internship_id']
    def __init__(self, user, *args, **kwargs):
        super(AddIntern, self).__init__(*args, **kwargs)
        self.fields['user_id'].queryset = UserDetails.objects.filter(user_role="INTERN", user_status="ACTIVE")


class AssignTopic(ModelForm):
    class Meta:
        model = AssignedTopics
        fields = '__all__'


class data(ModelForm):
    class Meta:
        model=Data
        fields=['data_content','data_reference']


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


class add_topic(forms.Form):
    # class Meta:
    #     model = Topic
    #     fields = ['topic_name']
    topic = forms.CharField(max_length=255, widget=forms.TextInput())


class add_subtopic(forms.Form):
    subtopic = forms.CharField(max_length=255, widget=forms.TextInput())

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
