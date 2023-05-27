from django.contrib import admin

# Register your models here.
from .models import DataStructure, DataStructureRequiredField


class DataStructureAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "lease_id",
    ]
    list_filter = [
        "user",
        "lease_id", ]
    search_fields = ('user',)


admin.site.register(DataStructure, DataStructureAdmin)


class DataStructureRequiredFieldAdmin(admin.ModelAdmin):
    list_display = [
        "lease_id",
    ]
    list_filter = [
        "lease_id", ]


admin.site.register(DataStructureRequiredField, DataStructureRequiredFieldAdmin)
