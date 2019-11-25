from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.conf import settings
from django.utils import timezone
from django.core.files import File


class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    no_of_days = models.IntegerField(default=0)
    is_email_verified = models.BooleanField(default=False)
    is_intern = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=255, blank=True, null=True)
    key_expiry_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return u"id: {0}| {1} {2} | {3} ".format(
            self.user.id,
            self.user.first_name,
            self.user.last_name,
            self.user.email
        )

