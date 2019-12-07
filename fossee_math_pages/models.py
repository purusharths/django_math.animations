from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime

status= (
    ("ACTIVE", "ACTIVE"),
    ("INACTIVE", "INACTIVE"),
    ("SUSPENDED", "SUSPENDED"),
)


class data(models.Model):
    user=models.IntegerField(default=False,null=False)
    subtopic=models.CharField(max_length=255,null=False)
    text = RichTextField(config_name='awesome_ckeditor')
    post_date=models.DateTimeField(default=datetime.now())
    aproval_ststus=models.BooleanField(default=False)

class AddUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, blank = False, null= False)
    email = models.EmailField(blank = False)
    topic = models.CharField(max_length=30, blank = False, null = False)
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
    date = models.CharField(max_length=30)
    temp_password = models.CharField(max_length=10)
    status=models.CharField(max_length=255,choices=status,default='INACTIVE')
    def __str__(self):
        return self.name

    
