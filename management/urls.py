from django.urls import path

from admin_dashboard.views import TranslatorView
from .views import UploadContractView, ContractDetailView, ContractDeleteView, UpdateAllContractAPIView, \
    ContractUpdateView, custom_logout, DownloadUploadCSVView, ContractListView, ContractDeleteWithIDView

urlpatterns = [
    path("upload/", UploadContractView.as_view(), name="upload_data"),
    path("", ContractListView.as_view(), name="contract"),
    path("custom_logout", custom_logout, name="custom_logout"),
    path("contract_update_api/<int:id>/", UpdateAllContractAPIView.as_view(), name="contract_update_api"),
    path("contract_delete/", ContractDeleteView.as_view(), name="contract_delete"),
    path("contract_delete/<int:id>/", ContractDeleteWithIDView.as_view(), name="contract_delete_with_id"),
    path("translate/", TranslatorView.as_view(), name="translate"),
    path("contract_detail/<int:id>/", ContractDetailView.as_view(), name="contract_detail"),
    path("contract_update/<int:id>/", ContractUpdateView.as_view(), name="contract_update"),
    path("contract_download/<int:id>/", DownloadUploadCSVView.as_view(), name="contract_download")
]
