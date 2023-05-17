from .models import DataStructure, DataStructureRequiredField
from django import forms


class DataStructureForm(forms.ModelForm):
    class Meta:
        model = DataStructure
        fields = "__all__"


class DataStructureRequiredFieldForm(forms.ModelForm):
    class Meta:
        model = DataStructureRequiredField
        fields = "__all__"
