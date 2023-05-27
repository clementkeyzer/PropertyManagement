from django.contrib.auth.mixins import UserPassesTestMixin


class AdminRequiredMixin(UserPassesTestMixin):
    """
    mixin for staff and admin
    """

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        if self.request.user.is_staff:
            return True
