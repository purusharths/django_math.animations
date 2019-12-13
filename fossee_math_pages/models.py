from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime
from django.utils.timezone import now

status = (
    ("ACTIVE", "ACTIVE"),
    ("INACTIVE", "INACTIVE"),
    ("SUSPENDED", "SUSPENDED"),
)

dataAprovalStatus = (
    ("PENDING", "PENDING"),
    ("APROVED", "APROVED"),
    ("REVIEW", "REVIEW"),
)


class data(models.Model):
    # config_name = 'awesome_ckeditor'
    user_id = models.IntegerField(default=False, null=False)
    subtopic = models.CharField(max_length=255, null=False)
    text = RichTextField(blank=True, null=True)
    post_date = models.DateTimeField(default=datetime.now())
    aproval_ststus = models.CharField(max_length=255, choices=dataAprovalStatus)

    def __str__(self):
        return self.subtopic


class AddUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(blank=False)
    topic = models.CharField(max_length=255, blank=True, null=True)
    phone = PhoneNumberField(null=False, blank=False, unique=True, default='+91')
    INTERN = 'INTERN'
    STAFF = 'STAFF'
    ROLE_TYPE = (
        (INTERN, 'Intern'),
        (STAFF, 'Staff'),

    )
    role = models.CharField(max_length=20,
                            choices=ROLE_TYPE,
                            default=INTERN)
    joined_date = models.DateTimeField(default=now, editable=False)
    temp_password = models.CharField(max_length=10)
    status = models.CharField(max_length=255, choices=status, default='INACTIVE')

    def __str__(self):
        return self.name
