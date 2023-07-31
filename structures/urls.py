from django.urls import path

from .views import DataStructureUpdateView, AdminUpdateRetrieveRequiredFieldsView, DataStructureRequiredFieldListView

urlpatterns = [
    path("", DataStructureUpdateView.as_view(), name="update_data_structure"),
    path('data_structure_required_fields/', DataStructureRequiredFieldListView.as_view(),
         name="data_structure_required_fields"),
    path("update_structure_required_fields/<int:id>/", AdminUpdateRetrieveRequiredFieldsView.as_view(),
         name="update_structure_required_fields")
]
