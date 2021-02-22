from django.contrib import admin
from .models import *
# Register your models here.

class ListAdmin(admin.ModelAdmin):
    list_display = ("List_name", "List_description")

admin.site.register(Listings, ListAdmin)
