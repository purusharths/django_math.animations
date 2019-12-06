from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

position_choices = (
    ("intern", "intern"),
    ("staff", "staff"),
)


class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now=True)
    is_email_verified = models.BooleanField(default=False)
    role = models.CharField(max_length=255, choices=position_choices, default='intern')
    activation_key = models.CharField(max_length=255, blank=True, null=True)
    key_expiry_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return u"id: {0} | {1} | {2} | {3} | {4}".format(
            self.user.id,
            self.user.first_name,
            self.user.last_name,
            self.user.email,
            self.role
        )


class data(models.Model):

    user=models.IntegerField(default=False)
    subtopic=models.TextField(null=False)
    content = RichTextField(config_name='awesome_ckeditor')


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
    def __str__(self):
        return self.name

    
