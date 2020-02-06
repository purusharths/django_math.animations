from datetime import datetime

from ckeditor_uploader.fields import RichTextUploadingField
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

    def __str__(self):
        return str(self.user_id) if self.user_id else ''


class Internship(models.Model):
    internship_topic = models.CharField(max_length=255, null=False)
    internship_thumbnail = models.ImageField(blank=False)
    internship_start_date = models.DateTimeField(default=datetime.now, blank=True)
    internship_status = models.CharField(max_length=20,
                                         choices=STATUS,
                                         default='INACTIVE')
    internship_quote = models.TextField(max_length=255)
    internship_quote_author = models.CharField(max_length=255)

    def __str__(self):
        return str(self.internship_topic) if self.internship_topic else ''


class Topic(models.Model):
    internship_id = models.ForeignKey(Internship, on_delete=models.CASCADE)
    user_id = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    topic_name = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.topic_name


class Subtopic(models.Model):
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    subtopic_name = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.subtopic_name


class Data(models.Model):
    subtopic_id = models.ForeignKey(Subtopic, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    data_content = RichTextUploadingField()
    data_reference = models.TextField(blank=True)
    data_post_date = models.DateTimeField(default=datetime.now, blank=True)
    data_status = models.CharField(max_length=20,
                                   choices=DATA_STATUS,
                                   default='WAITING')

    def __str__(self):
        return str(self.subtopic_id) if self.subtopic_id else ''


class DataVerification(models.Model):
    data_id = models.ForeignKey(Data, on_delete=models.CASCADE)
    dataverification_mentor = models.ForeignKey(User, on_delete=models.CASCADE)
    dataverification_verifier = models.CharField(max_length=255, blank=False)
    dataverification_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return str(self.data_id) if self.data_id else ''


class Chat(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    internship_id = models.ForeignKey(Internship, on_delete=models.CASCADE)
    chat_message = models.TextField(blank=False)
    chat_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return str(self.user_id) if self.user_id else ''


class Intern(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    internship_id = models.ForeignKey(Internship, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user_id) if self.user_id else ''


class AssignedTopics(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user_id) if self.user_id else ''
