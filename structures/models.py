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
    date_of_lease_date = models.CharField(max_length=250, blank=True, null=True, default="date_of_lease_date")
    first_day_of_term_date = models.CharField(max_length=240, blank=True, null=True, default="first_day_of_term_date")
    last_day_of_term_date = models.CharField(max_length=240, blank=True, null=True, default="last_day_of_term_date")
    lease_expiration_date = models.CharField(max_length=240, blank=True, null=True, default="lease_expiration_date")
    required_amount = models.CharField(max_length=250, blank=True, null=True, default="required_amount")
    security_type_code = models.CharField(max_length=250, blank=True, null=True, default="security_type_code")
    tenant_id = models.CharField(max_length=250, blank=True, null=True, default="tenant_id")
    tenant_name = models.CharField(max_length=250, blank=True, null=True, default="tenant_name")
    is_company = models.CharField(max_length=250, blank=True, null=True, default="is_company")
    from_date = models.CharField(max_length=240, blank=True, null=True, default="from_date")
    to_date = models.CharField(max_length=240, blank=True, null=True, default="to_date")
    type_code = models.CharField(max_length=250, blank=True, null=True,
                                 default="type_code")
    option_by_code = models.CharField(max_length=250, blank=True, null=True,
                                      default="option_by_code")
    term = models.CharField(max_length=250, blank=True, null=True, default="term")
    notice_term = models.CharField(max_length=250, blank=True, null=True, default="notice_term")
    notice_term_date = models.CharField(max_length=240, blank=True, null=True, default="notice_term_date")
    term_frequency = models.CharField(max_length=250, blank=True, null=True, default="term_frequency")
    fund_id = models.CharField(max_length=250, blank=True, null=True, default="fund_id")
    property_id = models.CharField(max_length=250, blank=True, null=True, default="property_id")
    unit_id = models.CharField(max_length=250, blank=True, null=True, default="unit_id")
    unit_type = models.CharField(max_length=250, blank=True, null=True, default="unit_type")
    gross_area = models.CharField(max_length=250, blank=True, null=True, default="gross_area")
    net_area = models.CharField(max_length=250, blank=True, null=True, default="net_area")
    vacant = models.CharField(max_length=250, blank=True, null=True, default="vacant")
    vacancy_note = models.CharField(max_length=250, blank=True, null=True, default="vacancy_note")
    # it required if is vacant is in there
    amount_rent = models.CharField(max_length=250, blank=True, null=True,
                                   default="amount_rent")
    amount_service_charge = models.CharField(max_length=250, blank=True, null=True,
                                             default="amount_service_charge")
    amount_others = models.CharField(max_length=250, blank=True, null=True,
                                     default="amount_others")
    amount_discount = models.CharField(max_length=250, blank=True, null=True,
                                       default="amount_discount")
    charge_frequency = models.CharField(max_length=250, blank=True, null=True, default="charge_frequency")
    vat_code = models.CharField(max_length=250, blank=True, null=True, default="vat_code")
    vat_rate = models.CharField(max_length=250, blank=True, null=True, default="vat_rate")
    vat_amount = models.CharField(max_length=250, blank=True, null=True, default="vat_amount")
    start_payment_schedule = models.CharField(max_length=240, blank=True, null=True, default="start_payment_schedule")
    end_payment_schedule = models.CharField(max_length=240, blank=True, null=True, default="end_payment_schedule")
    currency_code = models.CharField(max_length=250, blank=True, null=True, default="currency_code")
    index_series = models.CharField(max_length=250, blank=True, null=True, default="index_series")
    index_type = models.CharField(max_length=250, blank=True, null=True, default="index_type")
    start_date = models.CharField(max_length=240, blank=True, null=True, default="start_date")
    index_frequency = models.CharField(max_length=250, blank=True, null=True, default="index_frequency")

    index_date = models.CharField(max_length=240, blank=True, null=True, default="index_date")
    value = models.CharField(max_length=250, blank=True, null=True, default="value")
    value_sr2 = models.CharField(max_length=240, blank=True, null=True, default="value_sr2")
    index_date_sr2 = models.CharField(max_length=250, blank=True, null=True, default="index_date_sr2")

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
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    lease_id = models.BooleanField(default=True)
    date_of_lease_date = models.BooleanField(default=True)
    first_day_of_term_date = models.BooleanField(default=True)
    last_day_of_term_date = models.BooleanField(default=False)
    lease_expiration_date = models.BooleanField(default=True)
    required_amount = models.BooleanField(default=False)
    security_type_code = models.BooleanField(default=False)
    tenant_id = models.BooleanField(default=True)
    tenant_name = models.BooleanField(default=True)
    is_company = models.BooleanField(default=True)
    from_date = models.BooleanField(default=False)
    option_to_date = models.BooleanField(default=False)
    option_type_break_purchase_renew = models.BooleanField(default=False)
    option_type_landlord_tenant_mutual = models.BooleanField(default=False)
    term = models.BooleanField(default=False)
    notice_term = models.BooleanField(default=False)
    notice_term_date = models.BooleanField(default=False)
    term_frequency = models.BooleanField(default=False)
    fund_id = models.BooleanField(default=True)
    property_id = models.BooleanField(default=True)
    unit_id = models.BooleanField(default=True)
    unit_type = models.BooleanField(default=True)
    gross_area = models.BooleanField(default=True)
    net_area = models.BooleanField(default=True)
    vacant = models.BooleanField(default=True)
    vacancy_note = models.BooleanField(default=False)
    amount_rent = models.BooleanField(default=True)
    amount_service_charge = models.BooleanField(default=False)
    amount_others = models.BooleanField(default=False)
    income_category_discount_amount = models.BooleanField(default=False)
    charge_frequency = models.BooleanField(default=True)
    vat_code = models.BooleanField(default=True)
    vat_rate = models.BooleanField(default=True)
    vat_amount = models.BooleanField(default=True)
    start_payment_schedule = models.BooleanField(default=True)
    end_payment_schedule = models.BooleanField(default=False)
    currency_code = models.BooleanField(default=True)
    index_series = models.BooleanField(default=False)
    index_type = models.BooleanField(default=False)
    start_date = models.BooleanField(default=False)
    index_frequency = models.BooleanField(default=False)
    index_date = models.BooleanField(default=False)
    value = models.BooleanField(default=False)
    value_sr2 = models.BooleanField(default=False)
    index_date_sr2 = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)


def post_save_create_data_structure_required_fields(sender, instance, *args, **kwargs):
    """
    This creates a user data structurw once a user is being created
    :param instance:  the user created or updated
    """
    if instance:
        data_structure_required_fields = DataStructureRequiredField.objects.filter(user=instance).first()
        if not data_structure_required_fields:
            data_structure_required_fields = DataStructureRequiredField.objects.create(user=instance)


post_save.connect(post_save_create_data_structure_required_fields, sender=User)


def post_save_create_data_structure(sender, instance, *args, **kwargs):
    """
    This creates a user data structurw once a user is being created
    :param instance:  the user created or updated
    """
    if instance:
        data_structure = DataStructure.objects.filter(user=instance).first()
        if not data_structure:
            DataStructure.objects.create(user=instance)


post_save.connect(post_save_create_data_structure, sender=User)
