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

    # Char-field
    lease_id = models.CharField(max_length=250, blank=True, null=True)
    tenant_id = models.CharField(max_length=250, blank=True, null=True)
    tenant_name = models.CharField(max_length=250, blank=True, null=True)
    fund_id = models.CharField(max_length=250, blank=True, null=True)
    property_id = models.CharField(max_length=250, blank=True, null=True)
    unit_id = models.CharField(max_length=250, blank=True, null=True)
    unit_type = models.CharField(max_length=250, blank=True, null=True)
    # vacancy_reason to  vacancy_note
    vacancy_note = models.CharField(max_length=250, blank=True, null=True)
    # value_added_tax to vat_code
    vat_code = models.CharField(max_length=250, blank=True, null=True)
    # currency to currency_code
    currency_code = models.CharField(max_length=250, blank=True, null=True)
    index_type = models.CharField(max_length=250, blank=True, null=True)

    #  Date
    # lease_start_date to date_of_lease_date
    start_date = models.DateField(blank=True, null=True)
    date_of_lease_date = models.DateField(blank=True, null=True)
    first_day_of_term_date = models.DateField(blank=True, null=True)
    last_day_of_term_date = models.DateField(blank=True, null=True)
    lease_expiration_date = models.DateField(blank=True, null=True)
    # option_from_date to from_date
    from_date = models.DateField(blank=True, null=True)
    # option_to_date to to_date
    to_date = models.DateField(max_length=240, blank=True, null=True)
    notice_term_date = models.DateField(max_length=250, blank=True, null=True)
    start_payment_schedule = models.DateField(blank=True, null=True)
    end_payment_schedule = models.DateField(blank=True, null=True)
    # next_index_date to value_sr2
    index_date_sr2 = models.DateField(blank=True, null=True)
    index_date = models.DateField(blank=True, null=True)

    # Boolean Fields
    is_company = models.BooleanField(blank=True, null=True)
    # is_vacant to vacant
    vacant = models.BooleanField(blank=True, null=True)

    # Integer Fields
    # rent_security_type to security_type_code
    security_type_code = models.IntegerField(blank=True, null=True)
    # option_type_break_purchase_renew to type_code
    option_type_code = models.IntegerField(blank=True, null=True)
    # option_type_landlord_tenant_mutual to option_by_code
    option_by_code = models.IntegerField(blank=True, null=True)
    # notice_term_frequency to term_frequency
    term_frequency = models.IntegerField(blank=True, null=True)
    charge_frequency = models.IntegerField(blank=True, null=True)
    index_series = models.IntegerField(blank=True, null=True)
    index_frequency = models.IntegerField(blank=True, null=True)


    # rent_security to required_amount
    required_amount = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)

    term = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    notice_term = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)

    gross_area = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    net_area = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)

    # income_category_rent_amount to amount_rent
    amount_rent = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    # income_category_service_charges_amount to amount_service_charge
    amount_service_charge = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    # income_category_others_amount to amount_others
    amount_others = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    # income_category_discount_amount to amount_discount
    amount_discount = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)

    # value_added_tax_rate to vat_rate
    vat_rate = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    # added vat_amount
    vat_amount = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)


    # index_value to value
    value = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)

    # next_index_value to index_date_sr2
    value_sr2 = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
