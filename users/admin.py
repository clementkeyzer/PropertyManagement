from django.contrib import admin

# Register your models here.
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user",
                    "organisation_name",
                    "timestamp",)
    list_filter = ("user",
                   "organisation_name",
                   )
    search_fields = ('organisation_name',)


admin.site.register(UserProfile, UserProfileAdmin)
