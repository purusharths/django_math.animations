from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

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


class UserDetails(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    user_phone = PhoneNumberField(null=False, blank=False, unique=True, default='+91')
    INTERN = 'INTERN'
    STAFF = 'STAFF'
    ROLE_TYPE = (
        (INTERN, 'INTERN'),
        (STAFF, 'STAFF'),
    )
    user_role = models.CharField(max_length=20,
                                 choices=ROLE_TYPE,
                                 default=INTERN)
    user_temp_password = models.CharField(max_length=10, blank=True)
    user_status = models.CharField(max_length=255, choices=INTERN_STATUS, default='INACTIVE')


class Internship(models.Model):
    internship_topic = models.CharField(max_length=255, null=False)
    internship_thumbnail = models.ImageField(upload_to='thumbnails/', blank=False)
    internship_start_date = models.DateTimeField(default=datetime.now, blank=True)
    internship_status = models.CharField(max_length=20,
                                         choices=STATUS,
                                         default='INACTIVE')

    def __str__(self):
        return self.internship_topic


class Topic(models.Model):
    internship_id = models.ForeignKey(Internship, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    topic_name = models.CharField(max_length=255, null=False)


class Subtopic(models.Model):
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    subtopic_name = models.CharField(max_length=255, null=False)


class Data(models.Model):
    subtopic_id = models.ForeignKey(Subtopic, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    data_content = models.TextField(null=False)
    data_reference = models.TextField(blank=True)
    data_post_date = models.DateTimeField(default=datetime.now, blank=True)
    data_status = models.CharField(max_length=20,
                                   choices=DATA_STATUS,
                                   default='WAITING')


class DataVerification(models.Model):
    data_id = models.ForeignKey(Data, on_delete=models.CASCADE)
    dataverification_mentor = models.ForeignKey(User, on_delete=models.CASCADE)
    dataverification_verifier = models.CharField(max_length=255, blank=False)
    dataverification_date = models.DateTimeField(default=datetime.now, blank=True)


class Chat(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    internship_id = models.ForeignKey(Internship, on_delete=models.CASCADE)
    chat_message = models.TextField(blank=False)
    chat_date = models.DateTimeField(default=datetime.now, blank=True)


class Intern(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    internship_id = models.ForeignKey(Internship, on_delete=models.CASCADE)
