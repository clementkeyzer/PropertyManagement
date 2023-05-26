from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Contract(models.Model):
    """
    currently we are using two tables for the check this is used to get the history of thr data
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="contracts")
    status = models.CharField(max_length=250, default="PENDING", choices=(
        ("PENDING", "PENDING"),
        ("SUCCESS", "SUCCESS")
    ))
    name = models.CharField(max_length=250, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class Management(models.Model):
    """
    the datastructure of the property management
    """
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="managements")
    lease_id = models.CharField(max_length=250, )
    lease_start_date = models.DateField(blank=True, null=True)
    first_day_of_term_date = models.DateField(blank=True, null=True)
    last_day_of_term_date = models.DateField(blank=True, null=True)
    lease_expiration_date = models.DateField(blank=True, null=True)
    rent_security = models.CharField(max_length=250, blank=True, null=True)
    rent_security_type = models.CharField(max_length=250, blank=True, null=True)
    tenant_id = models.CharField(max_length=250, blank=True, null=True)
    tenant_name = models.CharField(max_length=250, blank=True, null=True)
    is_company = models.BooleanField(blank=True, null=True)
    option_from_date = models.DateField(blank=True, null=True)
    option_to_date = models.CharField(max_length=240, blank=True, null=True)
    option_type_break_purchase_renew = models.CharField(max_length=250, blank=True, null=True)
    option_type_landlord_tenant_mutual = models.CharField(max_length=250, blank=True, null=True)
    term = models.CharField(max_length=250, blank=True, null=True)
    notice_term = models.CharField(max_length=250, blank=True, null=True)
    notice_term_date = models.DateField(max_length=250, blank=True, null=True)
    notice_term_frequency = models.CharField(max_length=250, blank=True, null=True)
    fund_id = models.CharField(max_length=250, blank=True, null=True)
    property_id = models.CharField(max_length=250, blank=True, null=True)
    unit_id = models.CharField(max_length=250, blank=True, null=True)
    unit_type = models.CharField(max_length=250, blank=True, null=True)
    gross_area = models.CharField(max_length=250, blank=True, null=True)
    net_area = models.CharField(max_length=250, blank=True, null=True)
    is_vacant = models.BooleanField(blank=True, null=True)
    vacancy_reason = models.CharField(max_length=250, blank=True, null=True)
    # it required if is vacant is in there
    income_category_rent_amount = models.CharField(max_length=250, blank=True, null=True)
    income_category_service_charges_amount = models.CharField(max_length=250, blank=True, null=True)
    income_category_others_amount = models.CharField(max_length=250, blank=True, null=True)
    income_category_discount_amount = models.CharField(max_length=250, blank=True, null=True)
    term_frequency = models.CharField(max_length=250, blank=True, null=True)
    charge_frequency = models.CharField(max_length=250, blank=True, null=True)
    value_added_tax = models.CharField(max_length=250, blank=True, null=True)
    value_added_tax_rate = models.CharField(max_length=250, blank=True, null=True)
    start_payment_schedule = models.DateField(blank=True, null=True)
    end_payment_schedule = models.DateField(blank=True, null=True)
    currency = models.CharField(max_length=250, blank=True, null=True)
    index_series = models.CharField(max_length=250, blank=True, null=True)
    index_type = models.CharField(max_length=250, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    index_frequency = models.CharField(max_length=250, blank=True, null=True)
    index_date = models.DateField(blank=True, null=True)
    index_value = models.CharField(max_length=250, blank=True, null=True)
    next_index_date = models.DateField(blank=True, null=True)
    next_index_value = models.CharField(max_length=250, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    # added may 22
