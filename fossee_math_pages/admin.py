from django.contrib import admin
from .models import (UserDetails, Internship, Intern)

# # Register your models here.
# myModels = [AddUser,data]
# admin.site.register(myModels)

myModels = [UserDetails, Internship, Intern]
admin.site.register(myModels)