from django.contrib import admin
from .models import profile, AddIntern


# Register your models here.
class AddInternAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'topic')
    list_display_links = ('id', 'name')
admin.site.register(AddIntern, AddInternAdmin)
