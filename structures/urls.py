from django.urls import path

from .views import DataStructureUpdateView, AdminUpdateRetrieveRequiredFieldsView

urlpatterns = [
    path("", DataStructureUpdateView.as_view(), name="update_data_structure"),
    path("update_structure_required_fields", AdminUpdateRetrieveRequiredFieldsView.as_view(),
         name="update_structure_required_fields")
]
