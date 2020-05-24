#Admin Management
from django.contrib import admin

from .models import (UserDetails, Internship, Topic, Subtopic, Contributor, Data, ImageFormatting, Messages, HomeImages)

myModels = [UserDetails, Internship, Topic, Subtopic, Contributor, Data, ImageFormatting, Messages, HomeImages]

admin.site.register(myModels)
