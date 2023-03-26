from django.urls import path
from .views import ( UserRegistrationView, 
                    LogoutView,
                    UserLoginView,
                    UserList, 
                    UserDetail,
                    BankAccountTypeListCreateView,
                    BankAccountTypeRetrieveUpdateDestroyView,
                    UserBankAccountListCreateView,
                    UserBankAccountRetrieveUpdateDestroyView)

app_name = 'accounts'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/', LogoutView.as_view(), name='user_logout'),
    path('register/', UserRegistrationView.as_view(), name='user_registration'),
    path('users/', UserList.as_view(), name='user_list'), # eklendi
    path('users/<int:pk>/', UserDetail.as_view(), name='user_detail'), # eklendi
    path('bank-account-types/', BankAccountTypeListCreateView.as_view(), name='bank_account_type_list_create'),
    path('bank-account-types/<int:pk>/', BankAccountTypeRetrieveUpdateDestroyView.as_view(), name='bank_account_type_retrieve_update_destroy'),
    path('user-bank-accounts/', UserBankAccountListCreateView.as_view(), name='user_bank_account_list_create'),
    path('user-bank-accounts/<int:pk>/', UserBankAccountRetrieveUpdateDestroyView.as_view(), name='user_bank_account_retrieve_update_destroy'),
]
