from django.contrib import admin
from .models import (UserDetails, Internship, Intern, AssignedTopics, Data, Topic, Subtopic, Contributor, HomeImages)

myModels = [UserDetails, Internship, Intern, AssignedTopics, Data, Topic, Subtopic, Contributor, HomeImages]

admin.site.register(myModels)
