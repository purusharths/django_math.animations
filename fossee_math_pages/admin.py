from django.contrib import admin
from .models import (AddUser,data)

# Register your models here.
myModels = [AddUser,data]
admin.site.register(myModels)