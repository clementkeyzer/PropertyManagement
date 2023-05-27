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

    def __str__(self):
        return f"{self.name} - {self.user}"


class Management(models.Model):
    """
    the datastructure of the property management
    """
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="managements")
    lease_id = models.CharField(max_length=250, blank=True, null=True)
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


"""
How do i nake a model for something like this so user make rules Rules
IF gross_area is null or 0 THEN net_area must be > 0 
and the other way around as well: 
IF net_area is null or 0 THEN gross_area must be > 0
IF there is an option on the contract THEN it must be indicated how long the option lasts (with start and end date of the option)
 IF there is an option on the contract THEN a notice term must be entered
IF there is an index on the contract THEN there must also be an index date and an index type
IF there is a step rent THEN there must also be a start date for the next step rent ter (so there must be 2 values and 2 dates)"""


class ManagementRule(models.Model):
    """
    this is used to make rules which applies to each individual
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    gross_area_then_net_area = models.BooleanField(default=False)
    is_vacant_then_vacancy_reason = models.BooleanField(default=False)
    #  if the option type and by is provided then the date must also be provided
    option_then_date_provided = models.BooleanField(default=False)
    # if index_value and index_frequency is provided then the date must also be provided
    index_then_date = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
