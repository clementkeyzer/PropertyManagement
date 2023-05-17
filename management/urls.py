from django.urls import path

from .views import UploadDataView, ListContractView, ManagementListView, ContractDeleteView, create_user

urlpatterns = [
    path("", UploadDataView.as_view(), name="upload_data"),
    path('create_user/', create_user, name='create_user'),
    path("list_contract/", ListContractView.as_view(), name="list_contract"),
    path("contract_delete/", ContractDeleteView.as_view(), name="contract_delete"),
    path("list_contract/<int:id>/", ManagementListView.as_view(), name="list_contract_management")
]
