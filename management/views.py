import json

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import models
from django.db.models import BooleanField
from django.forms import formset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
from django.views import View
from django.views.generic import ListView

from structures.models import DataStructure
from .forms import UserCreationCustomForm, ManagementForm, ManagementRuleForm
from .models import Contract, Management, ManagementRule
from .utils import excel_to_dict_list, convert_string_int_to_bool, convert_string, query_items, \
    check_required_field_to_management, convert_file_to_dictionary, convert_date_format, check_validation_on_management

FormSet = formset_factory(ManagementForm, extra=0)


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
        Overiding context data
        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)
        # context['item_form'] = ManagementUpdate()
        context['exclude_management_fields'] = ["user", "contract", "id", "timestamp"]
        context["contract_id"] = self.kwargs['id']
        contract = Contract.objects.filter(id=self.kwargs['id']).first()

        #  new
        context["formset"] = [ManagementForm(instance=instance) for instance in contract.management_set.all()]
        context["contract"] = Contract.objects.filter(id=self.kwargs['id']).first()
        return context


class UpdateAllContractAPIView(View):
    """
    This view is used to update all fields from javasript post request using xml for the excel page
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

                if getattr(management_instance, field_name, field_value) != field_value:
                    # this set the attribute only if the value is not same with the old one and also saves it
                    setattr(management_instance, field_name, field_value)
            # Save the updated management instance for any update
            management_instance.save()

        return JsonResponse({'message': 'Update successful'})


class UploadContractView(LoginRequiredMixin, View):
    """
    this is used to upload excel spreadsheet which is then read and can be used to create tables

    """

    def get(self, request):
        contracts = Contract.objects.filter(user=self.request.user)
        context = {
            "contracts": contracts,
        }
        return render(request, "index.html", context)

    def post(self, request):
        global contract
        if request.method == 'POST' and request.FILES['property_file']:
            property_file = request.FILES['property_file']
            contract_name = request.POST.get("name")
            data_structure_id = DataStructure.objects.filter(user=self.request.user).first().id

            if not contract_name or not property_file or not data_structure_id:
                messages.warning(request, "Contract name or Excel File is required")
                return redirect("upload_data")

            try:
                contract = Contract.objects.create(name=contract_name, user=self.request.user)
                property_datas = convert_file_to_dictionary(property_file)

                for data in property_datas:
                    structure = DataStructure.objects.filter(id=data_structure_id, user=self.request.user).first()
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
                            setattr(management, field_name, convert_string_int_to_bool(management_value))
                        elif isinstance(management._meta.get_field(field_name), models.DateField):
                            setattr(management, field_name, convert_date_format(management_value))
                        else:
                            setattr(management, field_name, management_value)

                    management.contract = contract
                    management.user = self.request.user
                    management.save()

                return redirect("validate_contract", contract.id)
            except Exception as e:
                contract.delete()
                messages.error(request, f'Error uploading file: {e}')
                return redirect("upload_data")
        return redirect("upload_data")


class ContractRulesView(LoginRequiredMixin, View):
    """
    this is used to add rules to the contract  remove and the user is also able to view his or her rules
    """

    def get(self, request):
        """
        this is used to get the rules for the  management
        :param request:
        :return:
        """
        if ManagementRule.objects.count() < 1:
            management_rule = ManagementRule.objects.create(user=self.request.user)
        else:
            management_rule = ManagementRule.objects.filter(user=self.request.user).first()
        form = ManagementRuleForm(instance=management_rule)
        context = {
            "form": form,
            "management_rule": management_rule
        }
        return render(request, "management_rule.html", context)

    def post(self, request):
        """the post request"""
        management_rule = ManagementRule.objects.filter(user=self.request.user).first()

        form = ManagementRuleForm(data=self.request.POST, instance=management_rule)
        if form.is_valid():
            data_structure_form = form.save(commit=False)
            data_structure_form.user = self.request.user  # Assign the logged-in user
            data_structure_form.save()
            messages.success(request, "Successfully Update Structure")
        return redirect("contract_rules")


class ValidateContractView(LoginRequiredMixin, View):
    """
    this view is handling the validation of a contract, and it redirects the user to either the detail page or the
    update page base on the status of the contract
    """

    def get(self, request, id):
        contract = Contract.objects.filter(id=id).first()
        if not id:
            # redirect back to the page which  it comes from
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
        errors = []
        # First we check for required fields
        check_errors = check_required_field_to_management(contract)
        # user custom validation
        validate_errors = check_validation_on_management(contract)
        #  check if the length of the error is greater than zero if it is then
        #  we need to direct the user to the update page
        errors += check_errors
        errors += validate_errors
        if len(errors) > 0:
            contract.status = "PENDING"
            contract.save()
            for error in errors:
                messages.error(request, error)
            return redirect("contract_update", contract.id)
        contract.status = "SUCCESS"
        contract.save()
        messages.info(request, "The contract has been validated and currently has no errors")
        return redirect("contract_detail", contract.id)


@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def create_user(request):
    """
    this is used to create a new user
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = UserCreationCustomForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            username = email.split("@")[0]
            password = form.cleaned_data.get("password")
            confirm_password = form.cleaned_data.get("confirm_password")
            is_staff = form.cleaned_data.get("is_staff")
            is_superuser = form.cleaned_data.get("is_superuser")
            if password != confirm_password:
                messages.warning(request, "Password missmatch")
            if User.objects.filter(email=email).exists():
                messages.warning(request, "Email already exists")
            if is_superuser == True and request.user.is_superuser == False:
                #  a staff user must not be able to create a superuser
                messages.warning(request, "You dont have access to create a super user")
                return redirect('create_user')
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    is_staff=is_staff,
                    is_superuser=is_superuser)
                user.set_password(password)
                user.save()
                messages.info(request, "Successfully add user")
            return redirect('create_user')  # Redirect to a success page or any other URL
        else:
            messages.error(request, "An error Please provide the right data")
    else:
        form = UserCreationCustomForm()

    return render(request, 'added_user.html', {'form': form})
