from django.contrib import admin
from .models import profile


# Register your models here.

class AddIntern(admin.ModelAdmin):
    search_fields = ('Name', 'Topic')
    list_per_page = 20


admin.site.register(profile,AddIntern)
