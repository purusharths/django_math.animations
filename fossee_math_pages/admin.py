from django.contrib import admin
from .models import (UserDetails, Internship)

# # Register your models here.
# myModels = [AddUser,data]
# admin.site.register(myModels)

myModels = [UserDetails, Internship]
admin.site.register(myModels)