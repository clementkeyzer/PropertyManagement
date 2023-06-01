from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class AdminRequiredMixin(UserPassesTestMixin):
    """
    mixin for staff and admin
    """

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        if self.request.user.is_staff:
            return True
        messages.error(self.request, "You dont have permission to view the previous page")
        return redirect("upload_data")
