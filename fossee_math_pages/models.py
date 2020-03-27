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
    internship_thumbnail = models.ImageField(upload_to='images/', blank=False)
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
    subtopic_status = models.CharField(max_length=20,
                                       choices=DATA_STATUS,
                                       default='WAITING')

    def __str__(self):
        return self.subtopic_name


class Contributor(models.Model):
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE)
    contributor = models.CharField(max_length=255, null=False)
    mentor = models.CharField(max_length=255, null=False)
    professor = models.CharField(max_length=255, null=False)
    data_aproval_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.topic_id.topic_name, self.contributor, self.mentor, self.professor


class Data(models.Model):
    subtopic_id = models.ForeignKey(Subtopic, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    data_content = RichTextUploadingField()
    data_image = models.ImageField(upload_to='images/', blank=True, null=True)
    data_video = models.FileField(upload_to='media/', blank=True, null=True)
    data_post_date = models.DateTimeField(default=datetime.now, blank=True)
    data_status = models.CharField(max_length=20,
                                   choices=DATA_STATUS,
                                   default='WAITING')

    def __str__(self):
        return str(self.subtopic_id) if self.subtopic_id else ''


class ImageFormatting(models.Model):
    data_id = models.ForeignKey(Data, on_delete=models.CASCADE)
    image_height = models.CharField(max_length=5, default='100%')
    image_width = models.CharField(max_length=5, default='100%')

    def __str__(self):
        return self.data_id


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
