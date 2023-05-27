from django.contrib import admin
from .models import Contract, ManagementRule, Management


# Register your models here.

class ContractAdmin(admin.ModelAdmin):
    list_display = ("user",
                    "status",
                    "name",
                    "timestamp",)
    list_filter = ("user",
                   "status",
                   "name",)
    search_fields = ('status',)


admin.site.register(Contract, ContractAdmin)


class ManagementRuleAdmin(admin.ModelAdmin):
    list_display = ("user",
                    "gross_area_then_net_area",
                    "is_vacant_then_vacancy_reason",
                    "option_then_date_provided",
                    "timestamp",
                    )
    list_filter = ("user",
                   "gross_area_then_net_area",
                   "is_vacant_then_vacancy_reason",
                   "option_then_date_provided",)
    search_fields = ('user',)


admin.site.register(ManagementRule, ManagementRuleAdmin)


class ManagementRuleAdmin(admin.ModelAdmin):
    list_display = [
        "contract",
        "user",
        "lease_id",
    ]
    list_filter = [
        "contract",
        "user",
        "lease_id", ]
    search_fields = ('user',)


admin.site.register(Management, ManagementRuleAdmin)
