# forms.py
from django import forms
from .models import Management


class UserCreationCustomForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)
    confirm_password = forms.CharField(required=True)


class ManagementForm(forms.ModelForm):
    """
    this is the management form
    """

    class Meta:
        model = Management
        fields = "__all__"
