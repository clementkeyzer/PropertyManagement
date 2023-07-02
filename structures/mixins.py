from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class AdminRequiredMixin(UserPassesTestMixin):
    """
    mixin for staff and admin
    """

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        if self.request.user.is_superuser:
            return True
        if self.request.user.is_staff:
            return True
        return False

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect("account_login")
        if not self.request.user.is_superuser:
            return redirect("contract")
        if not self.request.user.is_staff:
            return redirect("contract")


class DisableAdminRequiredMixin(UserPassesTestMixin):
    """
 This is used to prevent dmin user  from accessing the main page
    """

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        if self.request.user.is_superuser:
            return False
        if self.request.user.is_staff:
            return False
        return True

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect("account_login")
        if self.request.user.is_superuser:
            return redirect("admin_dashboard")
        if self.request.user.is_staff:
            return redirect("admin_dashboard")
