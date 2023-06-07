from django.urls import path

from .views import UploadContractView, ContractDetailView, ContractDeleteView, UpdateAllContractAPIView, \
    ContractUpdateView, ValidateContractView, custom_logout, DownloadUploadCSVView

urlpatterns = [
    path("", UploadContractView.as_view(), name="upload_data"),
    path("custom_logout", custom_logout, name="custom_logout"),
    path("contract_update_api/<int:id>/", UpdateAllContractAPIView.as_view(), name="contract_update_api"),
    path("validate_contract/<int:id>/", ValidateContractView.as_view(), name="validate_contract"),
    path("contract_delete/", ContractDeleteView.as_view(), name="contract_delete"),
    path("contract_detail/<int:id>/", ContractDetailView.as_view(), name="contract_detail"),
    path("contract_update/<int:id>/", ContractUpdateView.as_view(), name="contract_update"),
    path("contract_download/<int:id>/", DownloadUploadCSVView.as_view(), name="contract_download")
]
