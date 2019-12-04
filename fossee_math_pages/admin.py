from django.contrib import admin
from .models import profile, AddUser


# Register your models here.
class AddUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'topic')
    list_display_links = ('id', 'name')

admin.site.register(AddUser, AddUserAdmin)
