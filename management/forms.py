# forms.py
from django import forms
from .models import Management, ManagementRule


class UserCreationCustomForm(forms.Form):
    """this form is used to create new user"""
    first_name = forms.SlugField(required=True)
    last_name = forms.SlugField(required=True)
    username = forms.SlugField(required=True)
    email = forms.EmailField(required=True)
    is_staff = forms.BooleanField(required=False)
    is_superuser = forms.BooleanField(required=False)
    password = forms.CharField(required=True)


class ManagementForm(forms.ModelForm):
    """
    this is the management form
    """
    #  all the date added here
    lease_start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%y-%m-%d'])
    first_day_of_term_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%y-%m-%d'])
    last_day_of_term_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%y-%m-%d'])
    lease_expiration_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%y-%m-%d'])
    option_from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%y-%m-%d'])
    option_to_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%y-%m-%d'])
    notice_term_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%y-%m-%d'])
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%y-%m-%d'])
    index_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%y-%m-%d'])
    next_index_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%y-%m-%d'])
    start_payment_schedule = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%y-%m-%d'])
    end_payment_schedule = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%y-%m-%d'])

    #  all the decimal add here
    rent_security = forms.DecimalField(max_digits=10, decimal_places=2,
                                       widget=forms.NumberInput(attrs={'class': 'form-control'}))
    option_type_break_purchase_renew = forms.DecimalField(max_digits=10, decimal_places=2,
                                                          widget=forms.NumberInput(attrs={'class': 'form-control'}))
    option_type_landlord_tenant_mutual = forms.DecimalField(max_digits=10, decimal_places=2,
                                                            widget=forms.NumberInput(attrs={'class': 'form-control'}))
    term = forms.DecimalField(max_digits=10, decimal_places=2,
                              widget=forms.NumberInput(attrs={'class': 'form-control'}))
    notice_term = forms.DecimalField(max_digits=10, decimal_places=2,
                                     widget=forms.NumberInput(attrs={'class': 'form-control'}))
    gross_area = forms.DecimalField(max_digits=10, decimal_places=2,
                                    widget=forms.NumberInput(attrs={'class': 'form-control'}))
    net_area = forms.DecimalField(max_digits=10, decimal_places=2,
                                  widget=forms.NumberInput(attrs={'class': 'form-control'}))
    income_category_rent_amount = forms.DecimalField(max_digits=10, decimal_places=2,
                                                     widget=forms.NumberInput(attrs={'class': 'form-control'}))
    income_category_service_charges_amount = forms.DecimalField(max_digits=10, decimal_places=2,
                                                                widget=forms.NumberInput(
                                                                    attrs={'class': 'form-control'}))
    income_category_others_amount = forms.DecimalField(max_digits=10, decimal_places=2,
                                                       widget=forms.NumberInput(attrs={'class': 'form-control'}))
    income_category_discount_amount = forms.DecimalField(max_digits=10, decimal_places=2,
                                                         widget=forms.NumberInput(attrs={'class': 'form-control'}))
    term_frequency = forms.DecimalField(max_digits=10, decimal_places=2,
                                        widget=forms.NumberInput(attrs={'class': 'form-control'}))
    charge_frequency = forms.DecimalField(max_digits=10, decimal_places=2,
                                          widget=forms.NumberInput(attrs={'class': 'form-control'}))
    value_added_tax = forms.DecimalField(max_digits=10, decimal_places=2,
                                         widget=forms.NumberInput(attrs={'class': 'form-control'}))
    value_added_tax_rate = forms.DecimalField(max_digits=10, decimal_places=2,
                                              widget=forms.NumberInput(attrs={'class': 'form-control'}))
    index_frequency = forms.DecimalField(max_digits=10, decimal_places=2,
                                         widget=forms.NumberInput(attrs={'class': 'form-control'}))
    index_value = forms.DecimalField(max_digits=10, decimal_places=2,
                                     widget=forms.NumberInput(attrs={'class': 'form-control'}))
    next_index_value = forms.DecimalField(max_digits=10, decimal_places=2,
                                          widget=forms.NumberInput(attrs={'class': 'form-control'}))
    notice_term_frequency = forms.DecimalField(max_digits=10, decimal_places=2,
                                               widget=forms.NumberInput(attrs={'class': 'form-control'}))

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
