from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.conf import settings
from django.utils import timezone
from django.core.files import File

position_choices = (
    ("intern", "intern"),
    ("staff", "staff"),
)

class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now=True)
    is_email_verified = models.BooleanField(default=False)
    role=models.CharField(max_length=255,choices=position_choices,default='intern')
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