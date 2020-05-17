# Django forms Management
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelForm

from .models import (UserDetails, Internship, Topic, Subtopic, Contributor, Data, ImageFormatting, Messages)

# Declaring Intern Status
INTERN_STATUS = (
    ("ACTIVE", "ACTIVE"),
    ("INACTIVE", "INACTIVE"),
)
# Declaring Status

STATUS = (
    ("ACTIVE", "ACTIVE"),
    ("INACTIVE", "INACTIVE"),
    ("COMPLETED", "COMPLETED"),
)
# Declaring data Status
DATA_STATUS = (
    ("ACCEPTED", "ACCEPTED"),
    ("REJECTED", "REJECTED"),
    ("WAITING", "WAITING"),
    ("UNDER REVIEW", "UNDER REVIEW"),
)


# Class definiton for userform1

class AddUserForm1(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


# Class definiton for userform2
class AddUserForm2(ModelForm):
    class Meta:
        model = UserDetails
        fields = ['user_phone', 'user_role', 'user_college']


# Class definiton for edituserform1
class EditUserForm1(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


# class definition for edituserform2
class EditUserForm2(ModelForm):
    class Meta:
        model = UserDetails
        fields = ['user_phone', 'user_college', 'user_bio']


# CLASS DECLRATION FOR EDIT BIO
class EditBio(ModelForm):
    class Meta:
        model = UserDetails
        fields = ['user_bio']


# CLASS DECLARATION FOR ADDINTERNSHIP FORM
class AddInternship(ModelForm):
    class Meta:
        model = Internship
        fields = ['internship_topic', 'internship_quote', 'internship_quote_author', 'internship_thumbnail',
                  'internship_status']

# CLASS DECLARATION FOR MANAGEINTERNSHIP
class ManageInternship(ModelForm):
    class Meta:
        model = Internship
        fields = ['internship_status']

# CLASS DECLARATION FOR APROVECONTENTS
class AproveContents(ModelForm):
    class Meta:
        model = Subtopic
        fields = ['subtopic_status']

# CLASS DECLARATION FOR ADD CONTRIBUTOR FORM
class AddContributor(ModelForm):
    class Meta:
        model = Contributor
        fields = ['mentor', 'professor']

# CLASS DECLARATION FOR EDITMEDIA FORM
class EditMedia(ModelForm):
    class Meta:
        model = Data
        fields = ['data_image', 'data_video', 'data_caption']

# CLASS DECLARATION FOR MANAGE INTERN FORM
class ManageIntern(ModelForm):
    class Meta:
        model = UserDetails
        fields = ['user_status']

# CLASS DECLARATION FOR TOPIC ORDER FORM
class topicOrder(ModelForm):
    class Meta:
        model = Topic
        fields = ['topic_order']

# CLASS DECLARATION FOR SUBTOPIC ORDER FORM
class subtopicOrder(ModelForm):
    class Meta:
        model = Subtopic
        fields = ['subtopic_order']

# CLASS FOR DATA FORM
class data(ModelForm):
    class Meta:
        model = Data
        fields = ['data_content']
        labels = {
            'data_content': "",
        }

# CLASS CHNAGE IMAGE FORM
class change_image(ModelForm):
    class Meta:
        model = Data
        fields = ['data_image', 'data_caption']  # 'data_video',
        labels = {
            'data_image': "Image",
            # 'data_video': "<br>OR<br><br>Video",
            'data_caption': "<br>Caption",
        }


class change_video(ModelForm):
    class Meta:
        model = Data
        fields = ['data_video', 'data_caption']  # 'data_image',
        labels = {
            'data_video': "Video",
            # 'data_image': "<br>OR<br><br>Image",
            'data_caption': "<br>Caption",
        }


class imageFormatting(ModelForm):
    class Meta:
        model = ImageFormatting
        fields = ['image_height', 'image_width']


class UserLoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput(render_value=False)
    )

    def clean(self):
        user = self.authenticate_via_email()
        if not user:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        else:
            self.user = user
        return self.cleaned_data

    def authenticate_user(self):
        return authenticate(
            username=self.user.username,
            password=self.cleaned_data['password'])

    def authenticate_via_email(self):
        """
            Authenticate user using email.
            Returns user object if authenticated else None
        """
        email = self.cleaned_data['email']
        if email:
            try:
                user = User.objects.get(email__iexact=email)
                if user.check_password(self.cleaned_data['password']):
                    return user
            except ObjectDoesNotExist:
                raise forms.ValidationError("Sorry, that login was invalid. Please try again.")

        return user


class add_topic(forms.Form):
    topic = forms.CharField(max_length=255, widget=forms.TextInput())


class add_subtopic(forms.Form):
    subtopic = forms.CharField(max_length=255, widget=forms.TextInput())


class addContributor(ModelForm):
    class Meta:
        model = Contributor
        fields = ['mentor', 'professor']


class sendMessage(ModelForm):
    class Meta:
        model = Messages
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'cols': 80, 'placeholder': "Send Message"}),

        }
        fields = ['message']
        labels = {"message": ""}
