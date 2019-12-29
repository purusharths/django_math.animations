from django.contrib import admin
from .models import (UserDetails)

# # Register your models here.
# myModels = [AddUser,data]
# admin.site.register(myModels)

myModels = [UserDetails]
admin.site.register(myModels)