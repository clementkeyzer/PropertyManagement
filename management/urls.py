from django.urls import path

from .views import UploadDataView, ManagementListView, ContractDeleteView, create_user, ManagementUpdateAllView

urlpatterns = [
    path("", UploadDataView.as_view(), name="upload_data"),
    path("update_all_management/<int:id>/", ManagementUpdateAllView.as_view(), name="update_all_management"),
    path('create_user/', create_user, name='create_user'),
    path("contract_delete/", ContractDeleteView.as_view(), name="contract_delete"),
    path("list_contract/<int:id>/", ManagementListView.as_view(), name="list_contract_management")
]
