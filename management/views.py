import json
import json
import re

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.db.models import BooleanField, ImageField, DateField
from django.forms import formset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView

from management.models import Contract, Management, ConverterTranslator
from structures.mixins import DisableAdminRequiredMixin
from structures.models import DataStructure
from .forms import ManagementForm
from .utils import convert_string_int_to_bool, convert_string, query_items, \
    check_required_field_to_management, convert_file_to_dictionary, convert_date_format, check_validation_on_management, \
    convert_string_to_int, check_header_in_structure, export_management_csv

FormSet = formset_factory(ManagementForm, extra=0)


def custom_logout(request):
    logout(request)
    return redirect('upload_data')  # Redirect to the desired URL after logout


class ContractDeleteView(View):
    """
    this is used to delete a Contract
    """

    def post(self, request):
        #  this  deletes a redirect back to the page
        item_id = request.POST.get("contract_id")
        if item_id:
            history = Contract.objects.filter(id=item_id, user=self.request.user).first()
            if history:
                history.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ContractDetailView(LoginRequiredMixin, ListView):
    """
    this is the detail page of the contract
    """
    queryset = Management.objects.all()
    template_name = "management.html"
    paginate_by = 1000

    def get_queryset(self):
        """
        Return the list of items for this view.

        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        id = self.kwargs['id']
        query = self.request.GET.get('search')

        contract = get_object_or_404(Contract, id=id)
        queryset = contract.management_set.all()
        ordering = self.get_ordering()
        if query:
            queryset = query_items(item=queryset, query=query)
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset

    def get_context_data(self, **kwargs):
        """
        Overiding context data
        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)
        context['exclude_management_fields'] = ["user", "contract", "id", "timestamp"]
        context["contract_id"] = self.kwargs['id']
        context["contract"] = Contract.objects.filter(id=self.kwargs['id']).first()
        return context


class ContractUpdateView(LoginRequiredMixin, ListView):
    """
    This is used to view the excel page to update the document
    """
    queryset = Management.objects.all()
    template_name = "management_edit.html"
    paginate_by = 1000

    def get_queryset(self):
        """
        Return the list of items for this view.

        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        id = self.kwargs['id']
        query = self.request.GET.get('search')

        contract = get_object_or_404(Contract, id=id)
        queryset = contract.management_set.all()
        ordering = self.get_ordering()
        if query:
            queryset = query_items(item=queryset, query=query)
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        return queryset

    def get_context_data(self, **kwargs):
        """
        Overriding context data
        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)
        # context['item_form'] = ManagementUpdate()
        context['exclude_management_fields'] = ["user", "contract", "id", "timestamp"]
        context["contract_id"] = self.kwargs['id']
        # the contract
        contract = Contract.objects.filter(id=self.kwargs['id']).first()

        # user custom validation
        validate_errors, instances_errors_1 = check_validation_on_management(contract)
        # First we check for required fields
        required_field_errors, instances_errors_2 = check_required_field_to_management(contract)
        # sort the errors
        validate_errors = sorted(validate_errors, key=lambda x: int(re.findall(r'\d+', x)[0]))
        required_field_errors = sorted(required_field_errors, key=lambda x: int(re.findall(r'\d+', x)[0]))

        instances_errors = instances_errors_1 + instances_errors_2
        #  new
        context["formset"] = [ManagementForm(instance=instance) for instance in contract.management_set.all()]
        context["contract"] = Contract.objects.filter(id=self.kwargs['id']).first()
        # send the both errors and other errors
        context["required_field_errors"] = required_field_errors
        context["validate_errors"] = validate_errors
        context["instances_errors"] = instances_errors
        #  add all the errors to check
        errors = instances_errors + validate_errors + required_field_errors
        if len(errors) > 0:
            contract.status = "PENDING"
            contract.save()
        else:
            contract.status = "SUCCESS"
            contract.save()
        return context


class UpdateAllContractAPIView(View):
    """
    This view is used to update all fields from javascript post request using xml for the Excel page
    """

    def post(self, request, id):
        contract_id = id
        # Check if the contract exists
        contract = Contract.objects.filter(id=contract_id).first()
        if not contract:
            return redirect("list_contract_management")

        # Retrieve the form data from the request body
        form_data = json.loads(request.body)

        # Perform the update operation for each form
        for form in form_data['forms']:
            form_id = form['id']
            form_fields = form['fields']

            # Retrieve the management instance based on the form ID
            management_instance = Management.objects.filter(id=form_id).first()
            if not management_instance:
                continue

            # Update the fields of the management instance
            for field_name, field_value in form_fields.items():
                #  if the  is among this just skip
                if field_name == "id" or field_name == "timestamp" or field_name == "user" or field_name == "contract":
                    continue
                #  if not value just skip
                if not field_value:
                    continue

                # Check if the field is a Boolean field
                field = Management._meta.get_field(field_name)
                if isinstance(field, BooleanField):
                    # Convert the field value to a Boolean
                    field_value = field_value.lower() == "true"
                # check if its a date field and has wrong value i set to none
                if isinstance(field, ImageField):
                    setattr(management_instance, field_name, convert_date_format(field_value))
                # if the value is not equal to  what is in the db i set to none
                if getattr(management_instance, field_name, field_value) != field_value:
                    # this set the attribute only if the value is not same with the old one and also saves it
                    # if its an date field validate it
                    if isinstance(field, DateField):
                        setattr(management_instance, field_name, convert_date_format(field_value))
                    else:
                        setattr(management_instance, field_name, field_value)
            # Save the updated management instance for any update
            management_instance.save()

        return JsonResponse({'message': 'Update successful'})


class ContractListView(LoginRequiredMixin, DisableAdminRequiredMixin, ListView):
    paginate_by = 10
    queryset = Contract.objects.all()
    template_name = "index.html"
    context_object_name = "contracts"

    def get_queryset(self):
        contract = Contract.objects.filter(user=self.request.user)
        return contract


class UploadContractView(LoginRequiredMixin, View):
    """
    this is used to upload Excel spreadsheet which is then read and can be used to create tables

    """

    def get(self, request):
        # redirect the user to admin dashboard
        if request.user.is_staff or request.user.is_superuser:
            return redirect("admin_dashboard")
        # create the structure for the user if not exists
        if not DataStructure.objects.filter(user=self.request.user).first():
            DataStructure.objects.create(user=self.request.user)
        # get the contract
        contracts = Contract.objects.filter(user=self.request.user)
        context = {
            "contracts": contracts,
        }
        return render(request, "index.html", context)

    def post(self, request):
        global contract
        if request.method == 'POST' and request.FILES['property_file']:
            property_file = request.FILES['property_file']
            clone_file = request.FILES['clone_file']
            contract_name = request.POST.get("name")

            if not contract_name or not property_file:
                messages.warning(request, "Contract name or Excel File is required")
                return redirect("upload_data")

            try:
                contract = Contract.objects.create(name=contract_name, user=self.request.user, file=clone_file)
                structure = DataStructure.objects.filter(user=self.request.user).first()

                property_datas, header_dictionary = convert_file_to_dictionary(property_file)
                #  validate the headers
                error_list = check_header_in_structure(headers=header_dictionary, structure=structure)
                # loop through the property data
                for data in property_datas:
                    management = Management()

                    for field in structure._meta.get_fields():
                        if field.name == "id" or field.name == "timestamp" or field.name == "user" or field.name == "contract":
                            continue

                        field_name = field.name
                        user_field_name = getattr(structure, field_name)
                        converted_field_name = convert_string(user_field_name)
                        management_value = data.get(converted_field_name)

                        #  we get attribute to be able to set the right value
                        if isinstance(management._meta.get_field(field_name), models.BooleanField):
                            # if it's a Boolean field
                            convert_qs = ConverterTranslator.objects.filter(convert_type="BOOLEAN",
                                                                            converted_string=convert_string(
                                                                                management_value)).first()
                            if convert_qs:
                                management_value = convert_qs.translate_to
                            setattr(management, field_name, convert_string_int_to_bool(management_value))
                        elif isinstance(management._meta.get_field(field_name), models.DateField):
                            # if it's a date time field
                            setattr(management, field_name, convert_date_format(management_value))
                        elif isinstance(management._meta.get_field(field_name), models.DecimalField):
                            # if it's a decimal field
                            convert_qs = ConverterTranslator.objects.filter(convert_type="DECIMAL",
                                                                            converted_string=convert_string(
                                                                                management_value)).first()
                            if convert_qs:
                                management_value = convert_qs.translate_to
                            setattr(management, field_name, convert_string_to_int(management_value))
                        elif isinstance(management._meta.get_field(field_name), models.IntegerField):
                            # if it's a integer field
                            convert_qs = ConverterTranslator.objects.filter(convert_type="INT",
                                                                            converted_string=convert_string(
                                                                                management_value)).first()
                            if convert_qs:
                                management_value = convert_qs.translate_to
                            setattr(management, field_name, convert_string_to_int(management_value))
                        elif isinstance(management._meta.get_field(field_name), models.CharField):
                            # if it's a integer field
                            convert_qs = ConverterTranslator.objects.filter(convert_type="STRING",
                                                                            converted_string=convert_string(
                                                                                management_value)).first()
                            if convert_qs:
                                management_value = convert_qs.translate_to
                            setattr(management, field_name, management_value)
                        else:
                            setattr(management, field_name, management_value)

                    management.contract = contract
                    management.user = self.request.user
                    management.save()
                # check if the length of the error is greater than 50 and if it is i delete
                if len(error_list) >= 50:
                    contract.delete()
                    messages.error(request, f'Error uploading file: So many errors with invalid header name')
                    return redirect("contract")
                if len(error_list) > 0:
                    for item in error_list:
                        messages.error(request, item)
                        # if the error is too much redirect back to home page to upload again
                    return redirect("contract_update", contract.id)
                else:
                    messages.info(request, "The contract has been validated and is error-free.")
                    return redirect("contract_detail", contract.id)
            except Exception as e:
                contract.delete()
                messages.error(request, f'Error uploading file: {e}')
                return redirect("contract")
        return redirect("contract")


class DownloadUploadCSVView(LoginRequiredMixin, View):
    """
    This is used to export the product to csv and return it to the frontend
    """

    def get(self, request, id):
        # The get request
        contract = Contract.objects.filter(id=id).first()
        if not contract:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        csv = export_management_csv(contract=contract)
        return csv
