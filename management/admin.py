from django.contrib import admin
from .models import Contract, ManagementRule, Management, RentSecurityDepositCode, OptionCode, OptionByCode, \
    ChargeFrequencyCode, CurrencyCode, UnitType, IndexFrequency, IndexSeriesCode, IndexType


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
    list_display = (
        "timestamp",
        "user",
        "gross_area_then_net_area",
        "is_vacant_then_vacancy_reason",
        "option_then_date_provided",

    )
    list_filter = ("user",
                   "gross_area_then_net_area",
                   "is_vacant_then_vacancy_reason",
                   "option_then_date_provided",)
    search_fields = ('user',)


admin.site.register(ManagementRule, ManagementRuleAdmin)


class ManagementRuleAdmin(admin.ModelAdmin):
    list_display = [
        "timestamp",
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


class RentSecurityDepositCodeRuleAdmin(admin.ModelAdmin):
    list_display = [
        "index",
        "value",
    ]
    list_filter = [
        "index",
        "value", ]
    search_fields = ('value',)


admin.site.register(RentSecurityDepositCode, RentSecurityDepositCodeRuleAdmin)


class OptionByCodeRuleAdmin(admin.ModelAdmin):
    list_display = [
        "index",
        "value",
    ]
    list_filter = [
        "index",
        "value", ]
    search_fields = ('value',)


admin.site.register(OptionByCode, OptionByCodeRuleAdmin)


class OptionCodeRuleAdmin(admin.ModelAdmin):
    list_display = [
        "index",
        "value",
    ]
    list_filter = [
        "index",
        "value", ]
    search_fields = ('value',)


admin.site.register(OptionCode, OptionCodeRuleAdmin)


class ChargeFrequencyCodeRuleAdmin(admin.ModelAdmin):
    list_display = [
        "index",
        "value",
    ]
    list_filter = [
        "index",
        "value", ]
    search_fields = ('value',)


admin.site.register(ChargeFrequencyCode, ChargeFrequencyCodeRuleAdmin)


class CurrencyCodeRuleAdmin(admin.ModelAdmin):
    list_display = [
        "index",
        "value",
    ]
    list_filter = [
        "index",
        "value", ]
    search_fields = ('value',)


admin.site.register(CurrencyCode, CurrencyCodeRuleAdmin)


class UnitTypeRuleAdmin(admin.ModelAdmin):
    list_display = [
        "index",
        "value",
    ]
    list_filter = [
        "index",
        "value", ]
    search_fields = ('value',)


admin.site.register(UnitType, UnitTypeRuleAdmin)


class IndexFrequencyRuleAdmin(admin.ModelAdmin):
    list_display = [
        "index",
        "value",
    ]
    list_filter = [
        "index",
        "value", ]
    search_fields = ('value',)


admin.site.register(IndexFrequency, IndexFrequencyRuleAdmin)


class IndexSeriesCodeRuleAdmin(admin.ModelAdmin):
    list_display = [
        "index",
        "value",
    ]
    list_filter = [
        "index",
        "value", ]
    search_fields = ('value',)


admin.site.register(IndexSeriesCode, IndexSeriesCodeRuleAdmin)


class IndexTypeRuleAdmin(admin.ModelAdmin):
    list_display = [
        "index",
        "value",
    ]
    list_filter = [
        "index",
        "value", ]
    search_fields = ('value',)


admin.site.register(IndexType, IndexTypeRuleAdmin)
