from django.db import models
from django.contrib.auth.models import User
from froala_editor.fields import FroalaField

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subtopic = models.CharField(max_length=255, blank=False);
    content = FroalaField()
    post_date = models.DateField()

class AddIntern(models.Model):
    upload_file = models.FileField()
    name = models.CharField(max_length=20)
    email = models.EmailField()
    topic = models.CharField(max_length=30)