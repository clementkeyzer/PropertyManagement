from datetime import datetime

from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.db import models
from django.db.models.signals import post_save, pre_save


def user_contract_file_upload_path(instance, filename):
    # Construct the file path based on the user's username and the original filename
    current_datetime = datetime.now()
    #  get a formatted date time for easy arrangement
    formatted_datetime = current_datetime.strftime("%Y-%m-%dT%H-%M")
    #  use the user organisation name for it
    organisation_name = str(instance.user.user_profile.organisation_name).replace(" ", "_")
    #  get the file extension
    file_extension = filename.split(".")[-1]
    return f'{organisation_name}/{formatted_datetime}__{instance.name}.{file_extension}'


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
    file = models.FileField(upload_to=user_contract_file_upload_path, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.name} - {self.user}"

    def delete(self, *args, **kwargs):
        # Delete the associated file before deleting the Contract instance
        if self.file:
            # Get the file path
            file_path = self.file.path

            # Delete the file from storage
            default_storage.delete(file_path)

        # Call the superclass delete() method to delete the instance
        super().delete(*args, **kwargs)


class Management(models.Model):
    """
    the datastructure of the property management
    """
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="managements")

    # Lease
    lease_id = models.CharField(max_length=250, blank=True, null=True)
    date_of_lease_date = models.DateField(blank=True, null=True)
    first_day_of_term_date = models.DateField(blank=True, null=True)
    last_day_of_term_date = models.DateField(blank=True, null=True)
    lease_expiration_date = models.DateField(blank=True, null=True)
    required_amount = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    security_type_code = models.IntegerField(blank=True, null=True)

    # tenant
    tenant_id = models.CharField(max_length=250, blank=True, null=True)
    tenant_name = models.CharField(max_length=250, blank=True, null=True)
    is_company = models.BooleanField(blank=True, null=True)

    # lease option
    from_date = models.DateField(blank=True, null=True)
    to_date = models.DateField(max_length=240, blank=True, null=True)
    option_type_code = models.IntegerField(blank=True, null=True)
    option_by_code = models.IntegerField(blank=True, null=True)
    term = models.IntegerField(blank=True, null=True)
    notice_term = models.IntegerField(blank=True, null=True)
    notice_term_date = models.DateField(max_length=250, blank=True, null=True)

    # unit
    fund_id = models.CharField(max_length=250, blank=True, null=True)
    property_id = models.CharField(max_length=250, blank=True, null=True)
    unit_id = models.CharField(max_length=250, blank=True, null=True)
    unit_type = models.CharField(max_length=250, blank=True, null=True)
    gross_area = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    net_area = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    vacant = models.BooleanField(blank=True, null=True)
    vacancy_note = models.CharField(max_length=250, blank=True, null=True)

    # lease charge
    amount_rent = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    amount_service_charge = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    amount_others = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    amount_discount = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    term_frequency = models.IntegerField(blank=True, null=True)
    charge_frequency = models.IntegerField(blank=True, null=True)
    vat_code = models.CharField(max_length=250, blank=True, null=True)
    vat_rate = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    vat_amount = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    start_payment_schedule = models.DateField(blank=True, null=True)
    end_payment_schedule = models.DateField(blank=True, null=True)
    currency_code = models.CharField(max_length=250, blank=True, null=True)

    #  index series
    index_series = models.IntegerField(blank=True, null=True)
    index_type = models.CharField(max_length=250, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    index_frequency = models.IntegerField(blank=True, null=True)
    index_date = models.DateField(blank=True, null=True)
    value = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    index_date_sr2 = models.DateField(blank=True, null=True)
    value_sr2 = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)

    timestamp = models.DateTimeField(auto_now_add=True)
    # value_added_tax to vat_code
    # currency to currency_code
    # lease_start_date to date_of_lease_date
    # option_from_date to from_date
    # option_to_date to to_date
    # next_index_date to value_sr2
    # is_vacant to vacant
    # rent_security_type to security_type_code
    # option_type_landlord_tenant_mutual to option_by_code
    # notice_term_frequency to term_frequency
    # rent_security to required_amount
    # income_category_rent_amount to amount_rent
    # income_category_service_charges_amount to amount_service_charge
    # income_category_others_amount to amount_others
    # income_category_discount_amount to amount_discount
    # value_added_tax_rate to vat_rate
    # added vat_amount
    # index_value to value
    # next_index_value to index_date_sr2


"""
How do i nake a model for something like this so user make rules Rules
IF gross_area is null or 0 THEN net_area must be > 0 
and the other way around as well: 
IF net_area is null or 0 THEN gross_area must be > 0
IF there is an option on the contract THEN it must be indicated how long the option lasts (with start and end date of the option)
 IF there is an option on the contract THEN a notice term must be entered
IF there is an index on the contract THEN there must also be an index date and an index type
IF there is a step rent THEN there must also be a start date for the next step rent ter (so there must be 2 values and 2 dates)
"""


class ManagementRule(models.Model):
    """
    this is used to make rules which applies to each individual
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    gross_area_then_net_area = models.BooleanField(default=True)
    is_vacant_then_vacancy_reason = models.BooleanField(default=True)
    vacant_required = models.BooleanField(default=True)
    #     1. we need a rule something like: IF Vacant = 0 THEN these fields are required:
    #         a. fund_id
    #         b. property_id
    #         c. unit_id
    #         d. unit_type
    #         e. is_vacant
    #         f. gross/net area
    #  if the option type and by is provided then the date must also be provided
    option_then_date_provided = models.BooleanField(default=True)
    # if value and index_frequency is provided then the date must also be provided
    index_then_date = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)


def post_save_create_management_rule(sender, instance, *args, **kwargs):
    """
    This creates a user  management rule once a user is being created
    :param instance:  the user created or updated
    """
    if instance:
        management_rule = ManagementRule.objects.filter(user=instance).first()
        if not management_rule:
            ManagementRule.objects.create(user=instance)


post_save.connect(post_save_create_management_rule, sender=User)


class ConverterTranslator(models.Model):
    """
    this is used to store multiple string and the translation to integer
    """
    converted_string = models.CharField(max_length=250, blank=True, null=True)
    convert_type = models.CharField(max_length=250, choices=(
        ("INT", "INT"),
        ("STRING", "STRING"),
        ("DECIMAL", "DECIMAL"),
        ("BOOLEAN", "BOOLEAN"),
    ))
    supplied_value = models.CharField(max_length=250, blank=True, null=True)
    translate_to = models.CharField(max_length=250)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["convert_type"]


def pre_save_create_converter_translator(sender, instance, *args, **kwargs):
    """
    This is used to update the converted string before being saved
    """
    from management.utils import convert_string

    if instance:
        instance.converted_string = convert_string(instance.supplied_value)


pre_save.connect(pre_save_create_converter_translator, sender=ConverterTranslator)


class RentSecurityDepositCode(models.Model):
    """
    this is used to convert values for editing security_type_code
    """
    index = models.CharField(max_length=250)
    value = models.CharField(max_length=250)


class OptionCode(models.Model):
    """
    this is used to set value for Option Type Code
    """
    index = models.CharField(max_length=250)
    value = models.CharField(max_length=250)


class OptionByCode(models.Model):
    """
    this is used to set value for Option by Code
    """
    index = models.CharField(max_length=250)
    value = models.CharField(max_length=250)


class ChargeFrequencyCode(models.Model):
    """
    this is used to set value for Option Type Code
    """
    index = models.CharField(max_length=250)
    value = models.CharField(max_length=250)


class CurrencyCode(models.Model):
    """
    this is used to set value for Option Type Code
    """
    index = models.CharField(max_length=250)
    value = models.CharField(max_length=250)


class UnitType(models.Model):
    """
    this is used to set value for Option Type Code
    """
    index = models.CharField(max_length=250)
    value = models.CharField(max_length=250)


class IndexFrequency(models.Model):
    """
    this is used to set value for Option Type Code
    """
    index = models.CharField(max_length=250)
    value = models.CharField(max_length=250)


class IndexSeriesCode(models.Model):
    """
    this is used to set value for Option Type Code
    """
    index = models.CharField(max_length=250)
    value = models.CharField(max_length=250)


class IndexType(models.Model):
    """
    this is used to set value for Option Type Code
    """
    index = models.CharField(max_length=250)
    value = models.CharField(max_length=250)
