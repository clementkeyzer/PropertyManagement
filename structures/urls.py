from django.urls import path

from .views import DataStructureCreateView, DataStructureUpdateView, UpdateRetrieveRequiredFieldsView

urlpatterns = [
    path("", DataStructureCreateView.as_view(), name="create_data_structure"),
    path("update_structure/<int:pk>/", DataStructureUpdateView.as_view(), name="update_data_structure"),
    path("update_structure_required_fields", UpdateRetrieveRequiredFieldsView.as_view(), name="update_structure_required_fields")
]
