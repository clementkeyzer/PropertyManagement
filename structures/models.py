from django.contrib.auth.models import User
from django.db import models

from django.db.models.signals import post_save


# Create your models here.


class DataStructure(models.Model):
    """
    the datastructure of the property management
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="data_structure")
    lease_id = models.CharField(max_length=250, blank=True, null=True, default="lease_id ")
    lease_start_date = models.CharField(max_length=250, blank=True, null=True, default="lease_start_date")
    first_day_of_term_date = models.CharField(max_length=240, blank=True, null=True, default="first_day_of_term_date")
    last_day_of_term_date = models.CharField(max_length=240, blank=True, null=True, default="last_day_of_term_date")
    lease_expiration_date = models.CharField(max_length=240, blank=True, null=True, default="lease_expiration_date")
    rent_security = models.CharField(max_length=250, blank=True, null=True, default="rent_security")
    rent_security_type = models.CharField(max_length=250, blank=True, null=True, default="rent_security_type")
    tenant_id = models.CharField(max_length=250, blank=True, null=True, default="tenant_id")
    tenant_name = models.CharField(max_length=250, blank=True, null=True, default="tenant_name")
    is_company = models.CharField(max_length=250, blank=True, null=True, default="is_company")
    option_from_date = models.CharField(max_length=240, blank=True, null=True, default="option_from_date")
    option_to_date = models.CharField(max_length=240, blank=True, null=True, default="option_to_date")
    option_type_break_purchase_renew = models.CharField(max_length=250, blank=True, null=True,
                                                        default="option_type_break_purchase_renew")
    option_type_landlord_tenant_mutual = models.CharField(max_length=250, blank=True, null=True,
                                                          default="option_type_landlord_tenant_mutual")
    term = models.CharField(max_length=250, blank=True, null=True, default="term")
    notice_term = models.CharField(max_length=250, blank=True, null=True, default="notice_term")
    notice_term_date = models.CharField(max_length=240, blank=True, null=True, default="notice_term_date")
    notice_term_frequency = models.CharField(max_length=250, blank=True, null=True, default="notice_term_frequency")
    fund_id = models.CharField(max_length=250, blank=True, null=True, default="fund_id")
    property_id = models.CharField(max_length=250, blank=True, null=True, default="property_id")
    unit_id = models.CharField(max_length=250, blank=True, null=True, default="unit_id")
    unit_type = models.CharField(max_length=250, blank=True, null=True, default="unit_type")
    gross_area = models.CharField(max_length=250, blank=True, null=True, default="gross_area")
    net_area = models.CharField(max_length=250, blank=True, null=True, default="net_area")
    is_vacant = models.CharField(max_length=250, blank=True, null=True, default="is_vacant")
    vacancy_reason = models.CharField(max_length=250, blank=True, null=True, default="vacancy_reason")
    # it required if is vacant is in there
    income_category_rent_amount = models.CharField(max_length=250, blank=True, null=True,
                                                   default="income_category_rent_amount")
    income_category_service_charges_amount = models.CharField(max_length=250, blank=True, null=True,
                                                              default="income_category_service_charges_amount")
    income_category_others_amount = models.CharField(max_length=250, blank=True, null=True,
                                                     default="income_category_others_amount")
    income_category_discount_amount = models.CharField(max_length=250, blank=True, null=True,
                                                       default="income_category_discount_amount")
    term_frequency = models.CharField(max_length=250, blank=True, null=True, default="term_frequency")
    charge_frequency = models.CharField(max_length=250, blank=True, null=True, default="charge_frequency")
    value_added_tax = models.CharField(max_length=250, blank=True, null=True, default="value_added_tax")
    value_added_tax_rate = models.CharField(max_length=250, blank=True, null=True, default="value_added_tax_rate")
    start_payment_schedule = models.CharField(max_length=240, blank=True, null=True, default="start_payment_schedule")
    end_payment_schedule = models.CharField(max_length=240, blank=True, null=True, default="end_payment_schedule")
    currency = models.CharField(max_length=250, blank=True, null=True, default="currency")
    index_series = models.CharField(max_length=250, blank=True, null=True, default="index_series")
    index_type = models.CharField(max_length=250, blank=True, null=True, default="index_type")
    start_date = models.CharField(max_length=240, blank=True, null=True, default="start_date")
    index_frequency = models.CharField(max_length=250, blank=True, null=True, default="index_frequency")

    index_date = models.CharField(max_length=240, blank=True, null=True, default="index_date")
    index_value = models.CharField(max_length=250, blank=True, null=True, default="index_value")
    next_index_date = models.CharField(max_length=240, blank=True, null=True, default="next_index_date")
    next_index_value = models.CharField(max_length=250, blank=True, null=True, default="next_index_value")

    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def form(self):
        from structures.forms import DataStructureForm
        if hasattr(self, '_form'):
            return self._form
        self._form = DataStructureForm(instance=self)
        return self._form





class DataStructureRequiredField(models.Model):
    """
    the datastructure of the property management
    """
    lease_id = models.BooleanField(default=True)
    lease_start_date = models.BooleanField(default=True)
    first_day_of_term_date = models.BooleanField(default=True)
    last_day_of_term_date = models.BooleanField(default=False)
    lease_expiration_date = models.BooleanField(default=True)
    rent_security = models.BooleanField(default=False)
    rent_security_type = models.BooleanField(default=False)
    tenant_id = models.BooleanField(default=True)
    tenant_name = models.BooleanField(default=True)
    is_company = models.BooleanField(default=True)
    option_from_date = models.BooleanField(default=False)
    option_to_date = models.BooleanField(default=False)
    option_type_break_purchase_renew = models.BooleanField(default=False)
    option_type_landlord_tenant_mutual = models.BooleanField(default=False)
    term = models.BooleanField(default=False)
    notice_term = models.BooleanField(default=False)
    notice_term_date = models.BooleanField(default=False)
    notice_term_frequency = models.BooleanField(default=False)
    fund_id = models.BooleanField(default=True)
    property_id = models.BooleanField(default=True)
    unit_id = models.BooleanField(default=True)
    unit_type = models.BooleanField(default=True)
    gross_area = models.BooleanField(default=True)
    net_area = models.BooleanField(default=True)
    is_vacant = models.BooleanField(default=True)
    vacancy_reason = models.BooleanField(default=False)
    income_category_rent_amount = models.BooleanField(default=True)
    income_category_service_charges_amount = models.BooleanField(default=False)
    income_category_others_amount = models.BooleanField(default=False)
    income_category_discount_amount = models.BooleanField(default=False)
    term_frequency = models.BooleanField(default=True)
    charge_frequency = models.BooleanField(default=True)
    value_added_tax = models.BooleanField(default=True)
    value_added_tax_rate = models.BooleanField(default=True)
    start_payment_schedule = models.BooleanField(default=True)
    end_payment_schedule = models.BooleanField(default=False)
    currency = models.BooleanField(default=True)
    index_series = models.BooleanField(default=False)
    index_type = models.BooleanField(default=False)
    start_date = models.BooleanField(default=False)
    index_frequency = models.BooleanField(default=False)
    index_date = models.BooleanField(default=False)
    index_value = models.BooleanField(default=False)
    next_index_date = models.BooleanField(default=False)
    next_index_value = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
