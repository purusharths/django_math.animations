from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelForm

from .models import (UserDetails, Internship, Topic, Subtopic, Contributor, Data, ImageFormatting, Messages, HomeImages)

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
        fields = ['internship_topic', 'internship_quote', 'internship_quote_author', 'internship_thumbnail',
                  'internship_status']


class ManageInternship(ModelForm):
    class Meta:
        model = Internship
        fields = ['internship_status']


class AproveContents(ModelForm):
    class Meta:
        model = Subtopic
        fields = ['subtopic_status']


class AddContributor(ModelForm):
    class Meta:
        model = Contributor
        fields = ['mentor', 'professor']


class EditMedia(ModelForm):
    class Meta:
        model = Data
        fields = ['data_image', 'data_video']


class ManageIntern(ModelForm):
    class Meta:
        model = UserDetails
        fields = ['user_status']


class topicOrder(ModelForm):
    class Meta:
        model = Topic
        fields = ['topic_order']


class subtopicOrder(ModelForm):
    class Meta:
        model = Subtopic
        fields = ['subtopic_order']


# class AddIntern(ModelForm):
#     class Meta:
#         model = Intern
#         labels = {
#             'user_id': 'Intern Name',
#             'internship_id': 'Internship Name'
#         }
#         fields = ['user_id', 'internship_id']
#
#     def __init__(self, user, *args, **kwargs):
#         super(AddIntern, self).__init__(*args, **kwargs)
#         self.fields['user_id'].queryset = UserDetails.objects.filter(user_role="INTERN", user_status="ACTIVE")
#         self.fields['internship_id'].queryset = Internship.objects.filter(internship_status='ACTIVE')

#
# class AssignTopic(ModelForm):
#     class Meta:
#         model = AssignedTopics
#         labels = {
#             'user_id': 'User',
#             'topic_d': 'Topic',
#         }
#         fields = ['user_id', 'topic_id']
#
#     def __init__(self, user, *args, **kwargs):
#         super(AssignTopic, self).__init__(*args, **kwargs)
#         assigned = AssignedTopics.objects.all().values_list('user_id_id')
#         qs = UserDetails.objects.filter(user_role="INTERN", user_status="ACTIVE").exclude(user_id_id__in=assigned)
#         self.fields['user_id'].queryset = qs
#         inner = AssignedTopics.objects.all().values_list('topic_id_id')
#         self.fields['topic_id'].queryset = Topic.objects.exclude(pk__in=inner)

class AssignTopic(ModelForm):
    class Meta:
        model = Subtopic
        fields = ['assigned_user_id']

    def __init__(self):
        super().__init__()
        self.fields['assigned_user_id'].queryset = User.objects.exclude(is_staff=True)


class data(ModelForm):
    class Meta:
        model = Data
        fields = ['data_content']


class imageFormatting(ModelForm):
    class Meta:
        model = ImageFormatting
        fields = ['image_height', 'image_width', 'image_caption']


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
        #mentor = forms.CharField(max_length=300, widget=forms.TextInput(attrs={"class":"md-textarea form-control", "id":"id_mentor"}))
        #professor = forms.CharField(max_length=300, widget=forms.TextInput(attrs={"class":"md-textarea form-control", "id":"id_professor"}))
        fields = ['mentor', 'professor']


class sendMessage(ModelForm):
    class Meta:
        model = Messages
        widgets = {
          'message': forms.Textarea(attrs={'rows':4, 'cols':15}),
        }
        fields = ['message']