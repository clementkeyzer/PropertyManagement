from django.urls import path

from .views import AdminUpdateUserMappingView, AdminDashboardView, AdminContractListView, AdminContractDeleteView, \
    AdminContractUpdateView, AdminContractRulesView, admin_create_user, AdminListUserView

urlpatterns = [
    path("admin_mapping", AdminUpdateUserMappingView.as_view(), name="admin_mapping"),
    path("dashboard", AdminDashboardView.as_view(), name="admin_dashboard"),
    path("admin_list_uploads", AdminContractListView.as_view(), name="admin_list_uploads"),
    path("admin_delete_contract", AdminContractDeleteView.as_view(), name="admin_delete_contract"),
    path("admin_contract_update/<int:id>/", AdminContractUpdateView.as_view(), name="admin_contract_update"),
    path('admin_contract_rules/', AdminContractRulesView.as_view(), name='admin_contract_rules'),
    path('admin_list_users/', AdminListUserView.as_view(), name='admin_list_users'),
    path('admin_create_user/', admin_create_user, name='admin_create_user'),

]
