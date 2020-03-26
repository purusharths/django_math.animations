from django.contrib import admin

from .models import (UserDetails, Internship, Intern, AssignedTopics, Data, Topic, Subtopic, Contributor)

# # Register your models here.
# myModels = [AddUser,data]
# admin.site.register(myModels)

myModels = [UserDetails, Internship, Intern, AssignedTopics, Topic, Subtopic, Contributor]
admin.site.register(myModels)

admin.site.register(Data)
