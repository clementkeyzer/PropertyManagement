from django.urls import path

from .views import UserProfileView, ChangeUserPassword

urlpatterns = [
    path("user_profile/", UserProfileView.as_view(), name="user_profile"),
    path("change_user_password/", ChangeUserPassword.as_view(), name="change_user_password"),
]
