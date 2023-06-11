from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from users.forms import UserProfileUpdateForm, ChangePasswordForm


# Create your views here.

class UserProfileView(LoginRequiredMixin, View):
    """
    this is used to get the user profile and also update it
    """

    def get(self, request):
        user_profile = self.request.user.user_profile
        form = UserProfileUpdateForm(instance=user_profile)
        change_form = ChangePasswordForm()
        context = {
            "form": form,
            "change_form": change_form,
            "user_profile": user_profile,
        }
        return render(request, "user_profile.html", context)

    def post(self, request):
        user_profile = self.request.user.user_profile
        form = UserProfileUpdateForm(data=self.request.POST, files=self.request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ChangeUserPassword(LoginRequiredMixin, View):

    def post(self, request):
        form = ChangePasswordForm(data=request.POST)
        if form.is_valid():
            password = form.cleaned_data.get("password")
            confirm_password = form.cleaned_data.get("confirm_password")
            if password != confirm_password:
                messages.error(request, "Password does not match")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            user = self.request.user
            user.set_password(password)
            user.save()
            messages.info(request, "Successfully Update password")
        else:
            for error in form.errors:
                messages.warning(request, f"{error}: {form.errors[error][0]}")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
