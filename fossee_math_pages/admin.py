from django.contrib import admin
from .models import profile, AddIntern


# Register your models here.
admin.site.register(profile)

class AddInternAdmin(admin.ModelAdmin):
    list_display = ('id', 'Name')
    list_display = ('id', 'Name')
    search_fields = ('Name', 'Topic')
    list_per_page = 20
admin.site.register(AddIntern, AddInternAdmin)