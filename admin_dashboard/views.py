import json

from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView

from admin_dashboard.utils import user_percentage_increase_since_last_month, \
    contract_percentage_increase_since_last_month
from management.forms import ManagementForm, ManagementRuleForm, ConverterTranslatorForm
from management.models import Contract, Management, ManagementRule, ConverterTranslator
from management.utils import query_items, is_integer_value
from structures.forms import DataStructureForm
from structures.mixins import AdminRequiredMixin
from structures.models import DataStructure
from users.forms import UserCreationCustomForm, AdminUpdateUserForm
from users.models import UserProfile

from .utils import lookup_excel_to_dict_list


# Create your views here.
class AdminDashboardView(LoginRequiredMixin, AdminRequiredMixin, View):
    """
    this is meant to view the analytics of the admin dashboard
    """

    def get(self, request):
        # counts
        contracts_count = Contract.objects.count()
        user_increment = user_percentage_increase_since_last_month()
        # percentage increment
        contract_increment = contract_percentage_increase_since_last_month()
        users_count = User.objects.count()
        # queryset top recent 5
        users = User.objects.all().order_by("-id")[:5]
        contracts = Contract.objects.all().order_by("-id")[:5]
        context = {
            "contracts_count": contracts_count,
            "users_count": users_count,
            "contract_increment": contract_increment,
            "user_increment": user_increment,
            "users": users,
            "contracts": contracts,
        }
        return render(request, "admin_dashboard.html", context)


class AdminUpdateUserMappingView(LoginRequiredMixin, AdminRequiredMixin, View):
    """
    This view is used to update all fields from javascript post request using xml for the excel page
    """

    def get(self, request):
        structures = DataStructure.objects.all()
        formset = [DataStructureForm(instance=instance) for instance in structures]
        exclude_management_fields = ["id", "timestamp"]
        context = {
            "structures": structures,
            "formset": formset,
            "exclude_management_fields": exclude_management_fields
        }
        return render(request, "admin_mapping.html", context)

    def post(self, request):

        # Retrieve the form data from the request body
        form_data = json.loads(request.body)

        # Perform the update operation for each form
        for form in form_data['forms']:
            form_id = form['id']
            form_fields = form['fields']

            # Retrieve the management instance based on the form ID
            management_instance = DataStructure.objects.filter(id=form_id).first()
            if not management_instance:
                continue

            # Update the fields of the management instance
            for field_name, field_value in form_fields.items():
                #  if the  is among this just skip
                if field_name == "id" or field_name == "timestamp" or field_name == "user":
                    continue
                #  if not value just skip
                if not field_value:
                    continue

                if getattr(management_instance, field_name, field_value) != field_value:
                    # this set the attribute only if the value is not same with the old one and also saves it
                    setattr(management_instance, field_name, field_value)
            # Save the updated management instance for any update
            management_instance.save()

        return JsonResponse({'message': 'Update successful'})


class AdminContractListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    queryset = Contract.objects.all().order_by("-id")
    template_name = "admin_contract.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        """
        Overiding context data
        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)
        context['exclude_management_fields'] = ["user", "contract", "id", "timestamp"]
        return context

    def get_queryset(self):
        """
        Return the list of items for this view.
        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        query = self.request.GET.get('search')
        ordering = self.get_ordering()
        queryset = self.queryset
        if query:
            queryset = query_items(item=queryset, query=query)
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        return queryset


class AdminContractDeleteView(LoginRequiredMixin, AdminRequiredMixin, View):
    """
    this is used to delete a Contract
    """

    def post(self, request):
        #  this  deletes a redirect back to the page
        item_id = request.POST.get("contract_id")
        if item_id:
            history = Contract.objects.filter(id=item_id).first()
            if history:
                history.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class AdminContractUpdateView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    """
    This is used to view the Excel page to update the document
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
        context['exclude_management_fields'] = ["user", "contract", "id", "timestamp"]
        context["contract_id"] = self.kwargs['id']
        contract = Contract.objects.filter(id=self.kwargs['id']).first()

        #  new
        context["formset"] = [ManagementForm(instance=instance) for instance in contract.management_set.all()]
        context["contract"] = Contract.objects.filter(id=self.kwargs['id']).first()
        return context


class AdminListUserView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    """
        This is used to view the users
        """
    queryset = User.objects.all().order_by("-id")
    template_name = "admin_added_user.html"
    paginate_by = 50

    def get_queryset(self):
        """
        Return the list of items for this view.

        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        query = self.request.GET.get('search')

        queryset = self.queryset.all()
        ordering = self.get_ordering()
        if query:
            queryset = User.objects.filter(username__icontains=query)
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
        context["form"] = UserCreationCustomForm()
        #  new
        return context


@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def admin_create_user(request):
    """
    this is used to create a new user
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = UserCreationCustomForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            username = form.cleaned_data.get("username")
            organisation_name = form.cleaned_data.get("organisation_name")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            password = form.cleaned_data.get("password")
            is_staff = form.cleaned_data.get("is_staff")
            is_superuser = form.cleaned_data.get("is_superuser")

            if User.objects.filter(email=email).exists():
                messages.warning(request, "Email already exists")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            if UserProfile.objects.filter(organisation_name__icontains=organisation_name).exists():
                messages.warning(request, "organisation name already exists")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            if User.objects.filter(username=username).exists():
                messages.warning(request, "Username already exists")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            if is_superuser == True and request.user.is_superuser == False:
                #  a staff user must not be able to create a superuser
                messages.warning(request, "You do not have sufficient privileges to create a superuser.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                user = User.objects.create(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    is_staff=is_staff,
                    is_superuser=is_superuser)
                user.set_password(password)
                user.save()
                user_profile = user.user_profile
                user_profile.organisation_name = organisation_name
                user_profile.save()
                messages.info(request, "Successfully add user")
        else:
            # if there was an error submitting the form
            for error in form.errors:
                messages.warning(request, f"{error}: {form.errors[error][0]}")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class AdminListUserRulesView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    queryset = ManagementRule.objects.all()
    paginate_by = 50
    template_name = "admin_list_user_rules.html"


class AdminContractRulesDetailView(LoginRequiredMixin, AdminRequiredMixin, View):
    """
    this is used to add rules to the contract  remove and the user is also able to view his or her rules
    """

    def get(self, request, id):
        """
        this is used to get the rules for the  management
        :param request:
        :return:
        """

        management_rule = ManagementRule.objects.filter(id=id).first()
        if not management_rule:
            messages.error(request, "Rule does not exist")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        form = ManagementRuleForm(instance=management_rule)
        context = {
            "form": form,
            "management_rule": management_rule
        }
        return render(request, "admin_management_rule.html", context)

    def post(self, request, id):
        """the post request"""
        management_rule = ManagementRule.objects.filter(id=id).first()
        user = management_rule.user
        if not management_rule:
            messages.error(request, "Rule does not exist")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        form = ManagementRuleForm(data=self.request.POST, instance=management_rule)
        if form.is_valid():
            management_rule_form = form.save(commit=False)
            management_rule_form.user = user
            management_rule_form.save()
            messages.success(request, "Successfully Update Structure")
        return redirect("admin_contract_rules")


class AdminUserProfileUpdateView(LoginRequiredMixin, AdminRequiredMixin, View):
    form_class = AdminUpdateUserForm
    template_name = 'admin_update_user.html'

    def get(self, request, id):
        user_profile = get_object_or_404(UserProfile, user_id=id)
        form = self.form_class(instance=user_profile)
        return render(request, "admin_update_user.html",
                      {'form': form, "user_profile": user_profile,
                       "user": user_profile.user})

    def post(self, request, id):
        user_profile = get_object_or_404(UserProfile, user_id=id)
        user = user_profile.user
        form = self.form_class(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            password = form.cleaned_data.get("password")
            if password is not None or password != "":
                user.set_password(password)
                user.save()
                if self.request.user == user:
                    user = authenticate(request, username=user.username, password=password,
                                        backend='django.contrib.auth.backends.ModelBackend')
                    if user is not None:
                        login(request, user)
            messages.info(request, "Successfully Update User")
        else:
            for error in form.errors:
                messages.warning(request, f"{error}: {form.errors[error][0]}")

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class AdminUserDeleteView(LoginRequiredMixin, AdminRequiredMixin, View):
    """
    this is used to delete a Contract
    """

    def post(self, request):
        #  this  deletes a redirect back to the page
        item_id = request.POST.get("user_id")
        if item_id:
            user = User.objects.filter(id=item_id).first()
            if user:
                user.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class TranslatorView(LoginRequiredMixin, AdminRequiredMixin, View):
    """
    this is used to convert to the translated words
    """

    def get(self, request):
        """
        this is used to  return the detail to translate
        :param request:
        :return:
        """
        translator_qs = ConverterTranslator.objects.all()
        excluded_fields = ["id", "converted_string", "timestamp"]

        formset = [ConverterTranslatorForm(instance=instance) for instance in translator_qs]
        context = {
            "formset": formset,
            "form": ConverterTranslatorForm(),
            "translator_qs": translator_qs,
            "excluded_fields": excluded_fields,
            "fields": ConverterTranslator._meta.fields
        }
        return render(request, "admin_translate.html", context)

    def post(self, request):

        # Retrieve the form data from the request body
        form_data = json.loads(request.body)

        # Perform the update operation for each form
        for form in form_data['forms']:
            form_id = form.get('id', None)
            form_fields = form['fields']

            if not form_fields.get("convert_type") or not form_fields.get("translate_to") or not form_fields.get(
                    "supplied_value"):
                continue
            if not form_id:
                convert_instance = ConverterTranslator()
            else:
                # Retrieve the management instance based on the form ID
                convert_instance = ConverterTranslator.objects.filter(id=form_id).first()
                if not convert_instance:
                    continue

            convert_instance.convert_type = form_fields.get("convert_type")
            convert_instance.translate_to = form_fields.get("translate_to")
            convert_instance.supplied_value = form_fields.get("supplied_value")
            # check if the convert type is int or decimal then the values it's translating to must be the same
            if convert_instance.convert_type == "INT" or convert_instance.convert_type == "DECIMAL":
                # check if the value can be changed to int
                if is_integer_value(convert_instance.translate_to):
                    # Save the updated management instance for any update
                    convert_instance.save()
                else:
                    messages.error(request, "Integer or decimal translate to cant be string")
            else:
                convert_instance.save()
        return JsonResponse({'message': 'Update successful'})


class ConverterTranslatorDeleteView(LoginRequiredMixin, AdminRequiredMixin, View):
    """
    this is used to delete a Contract
    """

    def post(self, request):
        #  this  deletes a redirect back to the page
        item_id = request.POST.get("convert_id")
        if item_id:
            convert = ConverterTranslator.objects.filter(id=item_id).first()
            if convert:
                convert.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ConvertUploadView(LoginRequiredMixin, AdminRequiredMixin, View):
    """
    this is used to make upadete to the look-up
    """

    def post(self, request):
        file = request.FILES.get("file")
        excel_file = lookup_excel_to_dict_list(file)
        row = 0
        for item in excel_file:
            row += 1
            convert_instance_qs = ConverterTranslator.objects.filter(
                convert_type=item.get("converttype"),
                supplied_value=item.get("suppliedvalue")
            )
            convert_instance = convert_instance_qs.first()
            if convert_instance_qs.count() > 1:
                # delete  other values and leave the first one
                # Delete the rest of the instances (excluding the first one)
                delete_instances = convert_instance_qs.exclude(id=convert_instance.id)
                delete_instances.delete()

            #  if the instance does not exist i make new one
            if not convert_instance:
                convert_instance = ConverterTranslator()
                convert_instance.supplied_value = item.get("suppliedvalue")
                convert_instance.convert_type = item.get("converttype", "STRING").upper()
            #  check if the type matches the translation to
            if item.get("converttype") == "INT" or item.get("converttype") == "DECIMAL":
                # check if the value can be changed to int
                if is_integer_value(item.get("translateto")):
                    # Save the updated management instance for any update
                    convert_instance.translate_to = item.get("translateto")
                    convert_instance.save()
                else:
                    messages.error(request, f"Row :{row} Translate to cant be string can only be Integer or decimal ")
            else:
                convert_instance.translate_to = item.get("translateto")
                convert_instance.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
