from datetime import datetime
from django.utils.timezone import now
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# default choices
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


# Additional table to store more details on the users.
# Foregin key from the default DJANGO User table
class UserDetails(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    user_phone = PhoneNumberField(null=True, blank=True, unique=False, default='+91')
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
    user_email = models.CharField(max_length=128)
    user_status = models.CharField(max_length=255, choices=INTERN_STATUS, default='INACTIVE')
    user_college = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.user_id) if self.user_id else ''


# table that will store the internship details,
class Internship(models.Model):
    internship_topic = models.CharField(max_length=255, null=False)
    internship_thumbnail = models.ImageField(upload_to='images/', blank=False)
    internship_start_date = models.DateTimeField(default=datetime.now, blank=True)
    internship_status = models.CharField(max_length=20,
                                         choices=STATUS,
                                         default='INACTIVE')
    internship_quote = models.TextField(max_length=255)
    internship_quote_author = models.CharField(max_length=128)
    internship_url = models.CharField(max_length=255)

    def __str__(self):
        return str(self.internship_topic) if self.internship_topic else ''


# table that will store the internship topics
# has a foregin key from the internship table
class Topic(models.Model):
    internship_id = models.ForeignKey(Internship, on_delete=models.CASCADE)
    topic_name = models.CharField(max_length=255, null=False)
    topic_url = models.CharField(max_length=255)
    topic_order = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.topic_name


# Saves the details of the subtopics in the topics and intrnship
# Foregin key from the topic table.
# Foregin key from the user table to store the assigned user details
class Subtopic(models.Model):
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE)
    assigned_user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    subtopic_name = models.CharField(max_length=255, null=False)
    subtopic_status = models.CharField(max_length=20,
                                       choices=DATA_STATUS,
                                       default='WAITING')
    subtopic_hash = models.CharField(max_length=50)
    subtopic_url = models.CharField(max_length=255)
    subtopic_modification_date = models.DateField(default=now)
    subtopic_order = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.subtopic_name


# Information storing the details of the contributor info
class Contributor(models.Model):
    subtopic_id = models.ForeignKey(Subtopic, on_delete=models.CASCADE)
    contributor = models.CharField(max_length=255, null=False)
    mentor = models.CharField(max_length=255, null=True, blank=True)
    professor = models.CharField(max_length=255, null=True, blank=True)
    data_aproval_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.topic_id.topic_name, self.contributor, self.mentor, self.professor


# saves the informatoin regarding the user submission for the subtopic
# foregin from the subtopic table
class Data(models.Model):
    subtopic_id = models.ForeignKey(Subtopic, on_delete=models.CASCADE)
    data_content = RichTextUploadingField()
    data_image = models.ImageField(upload_to='images/', blank=True, null=True)
    data_video = models.FileField(upload_to='video/', blank=True, null=True)
    data_caption = models.CharField(max_length=1024, blank=True, null=True)
    data_modification_date = models.DateTimeField(blank=True, null=True, default=now)
    data_hash = models.CharField(max_length=50)

    def __str__(self):
        return str(self.subtopic_id) if self.subtopic_id else ''


# stores the information regarding the image formatting
# firegin key from the data table
class ImageFormatting(models.Model):
    data_id = models.ForeignKey(Data, on_delete=models.CASCADE)
    image_height = models.CharField(max_length=5)
    image_width = models.CharField(max_length=5)


# table to stroe the data of the staff message to the interns
# have the foregin keys from the subtopic and user table info
class Messages(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    subtopic_id = models.ForeignKey(Subtopic, on_delete=models.CASCADE)
    message = models.TextField(max_length=300, null=True, blank=True)
    message_send_date = models.DateField(default=datetime.now, null=True, blank=True)

    def __str__(self):
        return str(self.subtopic_id) if self.subtopic_id else ''


# model to display the Home slider images (one instance of objects are expected to be added by the admin)
# Only one instance is entertained
class HomeImages(models.Model):
    image1 = models.ImageField(upload_to='home/', blank=True, null=True)
    image2 = models.ImageField(upload_to='home/', blank=True, null=True)
    image3 = models.ImageField(upload_to='home/', blank=True, null=True)
