from django.contrib import admin

# Register your models here.
from .models import DataStructure, DataStructureRequiredField


class DataStructureAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "lease_id",
        "lease_start_date",
        "first_day_of_term_date",
        "last_day_of_term_date",
    ]
    list_filter = [
        "user",
        "lease_id", ]
    search_fields = ('user',)


admin.site.register(DataStructure, DataStructureAdmin)


class DataStructureRequiredFieldAdmin(admin.ModelAdmin):
    list_display = [
        "lease_id",
        "lease_start_date",
        "first_day_of_term_date",
    ]
    list_filter = [
        "lease_id", ]


admin.site.register(DataStructureRequiredField, DataStructureRequiredFieldAdmin)
