from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
from django.views import View
from django.views.generic import ListView

from structures.models import DataStructure
from .forms import UserCreationCustomForm, ManagementForm
from .models import Contract, Management
from .utils import excel_to_dict_list, convert_string_int_to_bool, convert_string, query_items, \
    check_required_field_to_management
from django.forms import formset_factory, HiddenInput

FormSet = formset_factory(ManagementForm, extra=0)


class ContractDeleteView(View):
    """
    this is used to delete a Contract
    """

    def post(self, request):
        item_id = request.POST.get("contract_id")
        if item_id:
            history = Contract.objects.filter(id=item_id, user=self.request.user).first()
            if history:
                history.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ManagementListView(LoginRequiredMixin, ListView):
    queryset = Management.objects.all()
    template_name = "management.html"
    paginate_by = 50

    def get_queryset(self):
        """
        Return the list of items for this view.

        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        id = self.kwargs['id']
        query = self.request.GET.get('search')
        username = self.request.GET.get('username')

        contract = get_object_or_404(Contract, id=id)
        queryset = contract.management_set.all()
        ordering = self.get_ordering()
        if query:
            queryset = query_items(item=queryset, query=query)
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        if username:
            queryset = queryset.filter(user__username=username)

        return queryset

    def get_context_data(self, **kwargs):
        """
        Overiding context data
        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)
        # context['item_form'] = ManagementUpdate()
        context['exclude_management_fields'] = ["user", "contract", "id"]
        context["contract_id"] = self.kwargs['id']
        formset = FormSet(
            initial=Contract.objects.filter(id=self.kwargs['id']).first().management_set.all().values())
        # Hide a specific field
        for form in formset:
            form.fields['user'].widget = HiddenInput()
            form.fields['contract'].widget = HiddenInput()
        context["formset"] = formset
        context["contract"] = Contract.objects.filter(id=self.kwargs['id']).first()
        return context


class ManagementUpdateAllView(LoginRequiredMixin, View):

    def post(self, request, id):
        contract_id = id
        # check for the contract if it exists
        contract = Contract.objects.filter(id=contract_id).first()
        if not contract:
            return redirect("list_contract_management")
        # get all the managements
        managements = contract.management_set.all()
        formset = FormSet(request.POST)

        if formset.is_valid():
            for form, management in zip(formset, managements):
                form.instance.management = management  # Assign the current management instance to the form instance
                form.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class UploadDataView(LoginRequiredMixin, View):
    """
    this is used to upload exclel spreadsheet which is then read and can be used to create tables

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
            excel_file = request.FILES['property_file']
            contract_name = request.POST.get("name")
            data_structure_id = DataStructure.objects.filter(user=self.request.user).first().id

            if not contract_name or not excel_file or not data_structure_id:
                messages.warning(request, "Contract name or Excel File is required")
                return redirect("upload_data")

            try:
                excel_datas = excel_to_dict_list(excel_file)
                contract = Contract.objects.create(name=contract_name, user=self.request.user)

                for data in excel_datas:
                    structure = DataStructure.objects.filter(id=data_structure_id, user=self.request.user).first()
                    management = Management()

                    for field in structure._meta.get_fields():
                        if field.name == "id" or field.name == "timestamp" or field.name == "user" or field.name == "contract":
                            continue

                        field_name = field.name
                        user_field_name = getattr(structure, field_name)
                        converted_field_name = convert_string(user_field_name)
                        management_value = data.get(converted_field_name)

                        if isinstance(field, models.BooleanField):
                            setattr(management, field_name, convert_string_int_to_bool(management_value))
                        else:
                            setattr(management, field_name, management_value)

                    management.contract = contract
                    management.user = self.request.user
                    management.save()
                # Check for the required fields
                is_valid, field_name = check_required_field_to_management(contract)
                if not is_valid:
                    contract.delete()
                    messages.error(request, f"Field required on Excel {field_name}  ")
                    return redirect("upload_data")

                messages.info(request, 'Excel file uploaded successfully')
                return redirect("list_contract_management", contract.id)
            except Exception as e:
                contract.delete()
                messages.error(request, f'Error uploading Excel file: {e}')
                return redirect("upload_data")
        return redirect("upload_data")


@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def create_user(request):
    if request.method == 'POST':
        form = UserCreationCustomForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            username = email.split("@")[0]
            password = form.cleaned_data.get("password")
            confirm_password = form.cleaned_data.get("confirm_password")
            if password != confirm_password:
                messages.warning(request, "Password missmatch")
            if User.objects.filter(email=email).exists():
                messages.warning(request, "Email already exists")
            else:
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.save()
                messages.info(request, "Successfully add user")
            return redirect('create_user')  # Redirect to a success page or any other URL
        else:
            messages.error(request, "An error Please provide the right data")
    else:
        form = UserCreationCustomForm()

    return render(request, 'added_user.html', {'form': form})
