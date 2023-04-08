from django.urls import path
from .views import ( UserRegistrationView,
LogoutView,
UserLoginView,
UserList,
UserDetail,
BankAccountTypeListCreateView,
BankAccountTypeRetrieveUpdateDestroyView,
UserBankAccountListCreateView,
UserBankAccountRetrieveUpdateDestroyView,
UserAddressViewSet,
UserProfileViewSet,
UserProfileView,
UserBankAccountListCreateView,
AccountSettingsView,

)

app_name = 'accounts'

urlpatterns = [
path('login/', UserLoginView.as_view(), name='user_login'),
path('logout/', LogoutView.as_view(), name='user_logout'),
path('register/', UserRegistrationView.as_view(), name='user_registration'),
path('users/', UserList.as_view(), name='user_list'), # eklendi
path('users/int:pk/', UserDetail.as_view(), name='user_detail'), # eklendi
path('bank-account-types/', BankAccountTypeListCreateView.as_view(), name='bank_account_type_list_create'),
path('bank-account-types/int:pk/', BankAccountTypeRetrieveUpdateDestroyView.as_view(), name='bank_account_type_retrieve_update_destroy'),
path('user-bank-accounts/', UserBankAccountListCreateView.as_view(), name='user_bank_account_list_create'),
path('user-bank-accounts/int:pk/', UserBankAccountRetrieveUpdateDestroyView.as_view(), name='user_bank_account_retrieve_update_destroy'),
path('user-addresses/', UserAddressViewSet.as_view({'get': 'list', 'post': 'create'}), name='user_addresses'),
path('user-addresses/int:pk/', UserAddressViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='user_addresses_detail'),
path('user-profiles/', UserProfileViewSet.as_view({'get': 'list', 'post': 'create'}), name='user_profiles'),
path('user-profiles/int:pk/', UserProfileViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='user_profiles_detail'),
path('profile-settings/', UserProfileView.as_view(), name='profile_settings'),
 path('create-account/', UserBankAccountListCreateView.as_view(), name='create_account'),
 path('account-settings/', AccountSettingsView.as_view(), name='account_settings'),
]