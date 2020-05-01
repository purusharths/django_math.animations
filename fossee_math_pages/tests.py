from django.test import TestCase
from django.contrib.auth.models import User
from datetime import datetime
from .models import *


# Create your tests here.
class FosseeMathTest(TestCase):
    username_staff = "STAFF"
    email_staff = "STAFF@fossee.com"
    password_staff = "STAFF"
    phone_staff = "+919876787898"

    username_intern = "INTERN"
    email_intern = "INTERN@fossee.com"
    password_intern = "INTERN"
    phone_intern = "+919876787898"

    user_status = "ACTIVE"

    internship_topic = "TEST INTERNSHIP"
    internship_url = "test-internship"
    internship_status = "ACTIVE"
    internship_start_date = datetime.now()

    topic_name = "Topic 1"
    topic_url = "topic-1"

    subtopic_hash = "Subtopic 1"
    subtopic_name = "Subtopic 1"
    subtopic_url = "subtopic-1"
    subtopic_status = "WAITING"
    subtopic_modification_date = datetime.now()

    def Test_create_correct_user(self):
        form = User.objects.create_user(username=self.username_staff, email=self.email_staff,
                                        password=self.password_staff, is_staff=True)
        self.assertTrue(form)
        form = UserDetails.objects.create(user_id=form.pk, user_role='STAFF', user_email=self.email_staff,
                                          user_temp_password=self.password_staff, user_phone=self.phone_staff,
                                          user_status=self.user_status)
        self.assertTrue(form.is_valid())
        form = User.objects.create_user(username=self.username_intern, email=self.email_intern,
                                        password=self.password_intern, is_staff=False)
        self.assertTrue(form)
        form = UserDetails.objects.create(user_id=form.pk, user_role='INTERN', user_email=self.email_intern,
                                          user_temp_password=self.password_intern, user_phone=self.phone_intern,
                                          user_status=self.user_status)
        self.assertTrue(form.is_valid())

    def CreateInternship(self):
        internship = Internship.objects.create(internship_topic=self.internship_topic,
                                               internship_url=self.internship_url,
                                               internship_start_date=self.internship_start_date,
                                               internship_status=self.internship_status)
        self.assertTrue(internship.is_valid())
        topic = Topic.objects.create(internship_id_id=internship.pk, topic_name=self.topic_name,
                                     topic_url=self.topic_url)
        self.assertTrue(topic.is_valid())
        topic = Topic.objects.create(internship_id_id=internship.pk, topic_name=self.topic_name,
                                     topic_url=self.topic_url)
        self.assertFalse(topic.is_valid())
        assigned_user = User.objects.get(userdetails__user_role="INTERN")
        subtopic = Subtopic.objects.create(subtopic_hash=self.subtopic_hash, subtopic_name=self.subtopic_name,
                                           subtopic_url=self.subtopic_url, subtopic_status=self.subtopic_status,
                                           subtopic_modification_date=self.subtopic_modification_date,
                                           assigned_user_id=assigned_user.id)


