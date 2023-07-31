from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
from django.views import View
from django.views.generic import ListView

from .forms import DataStructureForm, DataStructureRequiredFieldForm
from .mixins import AdminRequiredMixin
from .models import DataStructure, DataStructureRequiredField
from .utils import query_required_field_items


class DataStructureUpdateView(LoginRequiredMixin, View):

    def get(self, request):
        if not DataStructure.objects.filter(user=self.request.user).first():
            DataStructure.objects.create(user=self.request.user)
        data_structure = DataStructure.objects.filter(user=self.request.user).first()
        form = DataStructureForm()
        context = {
            "form": form,
            "data_structure": data_structure,
        }
        return render(request, "data_structure.html", context=context)

    def post(self, request):
        data_structure = DataStructure.objects.filter(user=self.request.user).first()

        form = DataStructureForm(data=self.request.POST, instance=data_structure)
        if form.is_valid():
            data_structure = form.save(commit=False)
            data_structure.user = self.request.user  # Assign the logged-in user
            data_structure.save()
            messages.success(request, "Successfully Update Structure")
        return redirect("update_data_structure")


class DataStructureRequiredFieldListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    queryset = DataStructureRequiredField.objects.all()
    template_name = "admin_required_field_list.html"
    paginate_by = 50

    def get_queryset(self):
        """
        Return the list of items for this view.

        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        query = self.request.GET.get('search')

        queryset = DataStructureRequiredField.objects.all()
        ordering = self.get_ordering()
        if query:
            queryset = query_required_field_items(item=queryset, query=query)
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset


class AdminUpdateRetrieveRequiredFieldsView(LoginRequiredMixin, AdminRequiredMixin, View):
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
        return render(request, "admin_update_required_fields.html", context)

    def post(self, request):
        data_structure_required_field = DataStructureRequiredField.objects.first()
        form = DataStructureRequiredFieldForm(data=self.request.POST, instance=data_structure_required_field)
        if form.is_valid():
            form.save()
            messages.info(request, "Successfully Update Structure form")
        return redirect("update_structure_required_fields")


class AdminUpdateRetrieveRequiredFieldsView(LoginRequiredMixin, AdminRequiredMixin, View):
    """
    This is used to update required fields.
    """

    def get(self, request, id=None):
        # Check if the user has permission to set the required fields
        if not self.request.user.is_staff and not self.request.user.is_superuser:
            messages.info(request, "You don't have permission to set the required fields.")
            return redirect("upload_data")

        # Fetch the specific DataStructureRequiredField object based on the id parameter
        data_structure_required_fields = get_object_or_404(DataStructureRequiredField, id=id)

        form = DataStructureRequiredFieldForm(instance=data_structure_required_fields)
        context = {
            "form": form,
            "data_structure_required_fields": data_structure_required_fields,
        }
        return render(request, "admin_update_required_fields.html", context)

    def post(self, request, id=None):
        data_structure_required_field = get_object_or_404(DataStructureRequiredField, id=id)

        form = DataStructureRequiredFieldForm(data=request.POST, instance=data_structure_required_field)
        if form.is_valid():
            form.save()
            messages.info(request, "Successfully update required fields form")
        else:
            messages.error(request, "Error updating ")
        return redirect("update_structure_required_fields", id=id)
