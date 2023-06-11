import json
import random

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView

from admin_dashboard.utils import user_percentage_increase_since_last_month, \
    contract_percentage_increase_since_last_month
from management.forms import ManagementForm, ManagementRuleForm
from users.forms import UserCreationCustomForm
from management.models import Contract, Management, ManagementRule
from users.models import UserProfile
from management.utils import query_items, convert_string
from structures.forms import DataStructureForm
from structures.mixins import AdminRequiredMixin
from structures.models import DataStructure


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
            if UserProfile.objects.filter(organisation_name=organisation_name).exists():
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
