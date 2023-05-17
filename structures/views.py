from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
from django.views import View

from .forms import DataStructureForm, DataStructureRequiredFieldForm
from .models import DataStructure, DataStructureRequiredField


class DataStructureCreateView(LoginRequiredMixin, View):

    def get(self, request):
        form = DataStructureForm()
        context = {
            "form": form
        }
        return render(request, "data_structure.html", context=context)

    def post(self, request):
        form = DataStructureForm(data=self.request.POST)
        if form.is_valid():
            data_structure = form.save(commit=False)
            data_structure.user = self.request.user  # Assign the logged-in user
            data_structure.save()
            messages.success(request, "Successfully Create Structure")
        return redirect("create_data_structure")


class DataStructureUpdateView(LoginRequiredMixin, View):

    def post(self, request, **kwargs):
        id = self.kwargs.get("pk")
        data_structure = DataStructure.objects.filter(user=self.request.user, id=id).first()
        if not data_structure:
            messages.warning(request, "An error occurred ")
            return redirect("upload_data")

        form = DataStructureForm(instance=data_structure, data=request.POST)
        if form.is_valid():
            data_structure = form.save(commit=False)
            data_structure.user = self.request.user  # Assign the logged-in user
            data_structure.save()
            messages.info(request, "Successfully updated structure")
            return redirect("upload_data")  # Replace with your desired URL or view name

        messages.warning(request, "Structure does not exists")
        return redirect("upload_data")


class UpdateRetrieveRequiredFieldsView(LoginRequiredMixin, View):
    """
    this is used to update required fields
    """

    def get(self, request):
        # check if the user has permission to set the required fields
        if self.request.user.is_staff == False and self.request.user.is_superuser == False:
            messages.info(request, "You dont have permission to set the required fields")
            return redirect("upload_data")
        data_structure_required_fields = DataStructureRequiredField.objects.first()
        if not data_structure_required_fields:
            data_structure_required_fields = DataStructureRequiredField.objects.create()
        form = DataStructureRequiredFieldForm(instance=data_structure_required_fields)
        context = {
            "form": form
        }
        return render(request, "update_required_fields.html", context)

    def post(self, request):
        data_structure_required_field = DataStructureRequiredField.objects.first()
        form = DataStructureRequiredFieldForm(data=self.request.POST, instance=data_structure_required_field)
        if form.is_valid():
            form.save()
            messages.info(request, "Successfully Update Sructure form")
        return redirect("update_structure_required_fields")
