from django.urls import path

from .views import AdminUpdateUserMappingView, AdminDashboardView, AdminContractListView, AdminContractDeleteView, \
    AdminContractUpdateView, AdminContractRulesDetailView, admin_create_user, AdminListUserView, AdminListUserRulesView, \
    AdminUserProfileUpdateView, AdminUserDeleteView, ConverterTranslatorDeleteView

urlpatterns = [
    path("admin_mapping", AdminUpdateUserMappingView.as_view(), name="admin_mapping"),
    path("dashboard", AdminDashboardView.as_view(), name="admin_dashboard"),
    path("admin_list_uploads", AdminContractListView.as_view(), name="admin_list_uploads"),
    path("admin_update_user/<int:id>/", AdminUserProfileUpdateView.as_view(), name="admin_update_user"),
    path("admin_delete_user", AdminUserDeleteView.as_view(), name="admin_delete_user"),
    path("admin_delete_contract", AdminContractDeleteView.as_view(), name="admin_delete_contract"),
    path("admin_contract_update/<int:id>/", AdminContractUpdateView.as_view(), name="admin_contract_update"),
    path('admin_contract_rules/', AdminListUserRulesView.as_view(), name='admin_contract_rules'),
    path('admin_contract_rules_detail/<int:id>/', AdminContractRulesDetailView.as_view(),
         name='admin_contract_rules_detail'),
    path('admin_list_users/', AdminListUserView.as_view(), name='admin_list_users'),
    path('convert_delete/', ConverterTranslatorDeleteView.as_view(), name='convert_delete'),
    path('admin_create_user/', admin_create_user, name='admin_create_user'),

]
