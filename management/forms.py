# forms.py
from django import forms

from .models import Management, ManagementRule, ConverterTranslator, RentSecurityDepositCode, OptionCode, OptionByCode, \
    ChargeFrequencyCode, CurrencyCode, UnitType, IndexFrequency, IndexSeriesCode, IndexType


class YesNoSelectWidget(forms.Select):

    def create_option(self, *args, **kwargs):
        option = super().create_option(*args, **kwargs)
        if option['value'] == '1':
            option['label'] = 'Yes'
        elif option['value'] == '2' or option['value'] == '0':
            option['label'] = 'No'
        return option


class CustomSelectTypeCodeWidget(forms.Select):
    def create_option(self, *args, **kwargs):
        value = kwargs.pop('value', None)
        option = super().create_option(*args, **kwargs)
        option_value = str(option['value'])

        for choice_value, choice_label in self.choices:
            if option_value == choice_value:
                option['label'] = choice_label
                break

        return option


class ManagementForm(forms.ModelForm):
    """
    this is the management form
    """
    #  all the date added here
    date_of_lease_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%y-%m-%d'])
    first_day_of_term_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%y-%m-%d'])
    last_day_of_term_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%y-%m-%d'])
    lease_expiration_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%y-%m-%d'])
    from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%y-%m-%d'])
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%y-%m-%d'])
    notice_term_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%y-%m-%d'])
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%y-%m-%d'])
    index_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%y-%m-%d'])
    start_payment_schedule = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%y-%m-%d'])
    end_payment_schedule = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%y-%m-%d'])
    index_date_sr2 = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%y-%m-%d'])

    #  all the decimal add here
    required_amount = forms.DecimalField(max_digits=10, decimal_places=2,
                                         widget=forms.NumberInput(attrs={'class': 'form-control'}))

    term = forms.DecimalField(max_digits=10, decimal_places=2,
                              widget=forms.NumberInput(attrs={'class': 'form-control'}))
    notice_term = forms.DecimalField(max_digits=10, decimal_places=2,
                                     widget=forms.NumberInput(attrs={'class': 'form-control'}))
    gross_area = forms.DecimalField(max_digits=10, decimal_places=2,
                                    widget=forms.NumberInput(attrs={'class': 'form-control'}))
    net_area = forms.DecimalField(max_digits=10, decimal_places=2,
                                  widget=forms.NumberInput(attrs={'class': 'form-control'}))
    amount_rent = forms.DecimalField(max_digits=10, decimal_places=2,
                                     widget=forms.NumberInput(attrs={'class': 'form-control'}))
    amount_service_charge = forms.DecimalField(max_digits=10, decimal_places=2,
                                               widget=forms.NumberInput(
                                                   attrs={'class': 'form-control'}))
    amount_others = forms.DecimalField(max_digits=10, decimal_places=2,
                                       widget=forms.NumberInput(attrs={'class': 'form-control'}))
    amount_discount = forms.DecimalField(max_digits=10, decimal_places=2,
                                         widget=forms.NumberInput(attrs={'class': 'form-control'}))

    # changed this
    # vat_code = forms.DecimalField(max_digits=10, decimal_places=2,
    #                               widget=forms.NumberInput(attrs={'class': 'form-control'})
    #                               )
    vat_code = forms.ChoiceField(
        widget=YesNoSelectWidget(attrs={'class': 'form-control'}),
        choices=[('1', 'Yes'), ('0', 'No')]
    )
    vat_rate = forms.DecimalField(max_digits=10, decimal_places=2,
                                  widget=forms.NumberInput(attrs={'class': 'form-control'}))
    vat_amount = forms.DecimalField(max_digits=10, decimal_places=2,
                                    widget=forms.NumberInput(attrs={'class': 'form-control'}))

    value = forms.DecimalField(max_digits=10, decimal_places=2,
                               widget=forms.NumberInput(attrs={'class': 'form-control'}))
    value_sr2 = forms.DecimalField(max_digits=10, decimal_places=2,
                                   widget=forms.NumberInput(attrs={'class': 'form-control'}))

    # integer field
    # change this field
    # option_type_code = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    option_type_code = forms.ChoiceField(
        widget=CustomSelectTypeCodeWidget(attrs={'class': 'form-select'}),
        choices=[("", 'Select'), *[(entry.index, entry.value) for entry in OptionCode.objects.all()]]
    )
    # changed this
    # charge_frequency = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    charge_frequency = forms.ChoiceField(
        widget=CustomSelectTypeCodeWidget(attrs={'class': 'form-select'}),
        choices=[("", 'Select'), *[(entry.index, entry.value) for entry in ChargeFrequencyCode.objects.all()]]
    )
    # changed this
    # option_by_code = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    option_by_code = forms.ChoiceField(
        widget=CustomSelectTypeCodeWidget(attrs={'class': 'form-select'}),
        choices=[("", 'Select'), *[(entry.index, entry.value) for entry in OptionByCode.objects.all()]]
    )
    # changed this
    # index_series = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    index_series = forms.ChoiceField(
        widget=CustomSelectTypeCodeWidget(attrs={'class': 'form-select'}),
        choices=[("", 'Select'), *[(entry.index, entry.value) for entry in IndexSeriesCode.objects.all()]]
    )
    # changed this
    # security_type_code = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    security_type_code = forms.ChoiceField(
        widget=CustomSelectTypeCodeWidget(attrs={'class': 'form-select'}),
        choices=[("", 'Select'), *[(entry.index, entry.value) for entry in RentSecurityDepositCode.objects.all()]]
    )

    # changed this
    currency_code = forms.ChoiceField(
        widget=CustomSelectTypeCodeWidget(attrs={'class': 'form-select'}),
        choices=[("", 'Select'), *[(entry.index, entry.value) for entry in CurrencyCode.objects.all()]]
    )
    unit_type = forms.ChoiceField(
        widget=CustomSelectTypeCodeWidget(attrs={'class': 'form-select'}),
        choices=[("", 'Select'), *[(entry.index, entry.value) for entry in UnitType.objects.all()]]
    )

    # changed this
    # term_frequency = forms.IntegerField(
    #     widget=forms.NumberInput(attrs={'class': 'form-control'}),
    # )
    term_frequency = forms.ChoiceField(
        widget=CustomSelectTypeCodeWidget(attrs={'class': 'form-select'}),
        choices=[("", 'Select'), *[(entry.index, entry.value) for entry in ChargeFrequencyCode.objects.all()]]
    )
    # changed this
    # index_frequency = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    index_frequency = forms.ChoiceField(
        widget=CustomSelectTypeCodeWidget(attrs={'class': 'form-select'}),
        choices=[("", 'Select'), *[(entry.index, entry.value) for entry in IndexFrequency.objects.all()]]
    )
    # changed this
    index_type = forms.ChoiceField(
        widget=CustomSelectTypeCodeWidget(attrs={'class': 'form-select'}),
        choices=[("", 'Select'), *[(entry.index, entry.value) for entry in IndexType.objects.all()]]
    )

    class Meta:
        model = Management
        fields = "__all__"

        widgets = {
            'date_field': forms.DateInput(format='%y-%m-%d'),  # Specify the desired display format for the date field
        }


class ManagementRuleForm(forms.ModelForm):
    """
    this  form is used to update rules
    """

    class Meta:
        model = ManagementRule
        fields = "__all__"


class ConverterTranslatorForm(forms.ModelForm):
    """
    this is used to update or create the convert transal
    """

    class Meta:
        model = ConverterTranslator
        fields = "__all__"
