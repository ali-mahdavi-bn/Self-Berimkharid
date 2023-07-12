from django.urls import path

from accounts.apis.CustomerView import CustomerSendCodeView, CustomerRegisterView, CustomerLoginWithPasswordView, \
    CustomerLoginWithCodeView

from accounts.apis.SellerView import SellerSendCodeView, SellerRegisterView, SellerLoginView, \
    SellerRestPasswordView
from accounts.apis.AdminView import AdminLoginWithPasswordView,AdminRegisterView
from accounts.apis.AccountView import AccountInfoView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    # customer
    path('customer/sendCode/', CustomerSendCodeView.as_view(), name='send_code_customer'),
    path('customer/register/', CustomerRegisterView.as_view(), name='register_customer'),
    path('customer/loginWithPassword/', CustomerLoginWithPasswordView.as_view(), name='Login_with_password_customer'),
    path('customer/loginWihtCode/', CustomerLoginWithCodeView.as_view(), name='rest_password_customer'),

    # seller
    path('seller/sendCode/', SellerSendCodeView.as_view(), name='send_code_seller'),
    path('seller/register/', SellerRegisterView.as_view(), name='register_seller'),
    path('seller/login/', SellerLoginView.as_view(), name='Login_with_password_seller'),
    path('seller/restPassword/', SellerRestPasswordView.as_view(), name='rest_password_seller'),

    # admin
    path('admin/LoginWithPassword/', AdminLoginWithPasswordView.as_view(), name='Login_with_password_admin'),
    # path('admin/register/', AdminRegisterView.as_view(), name='admin_register'),

    # account
    path('account/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('account/userInfo/', AccountInfoView.as_view(), name='user_info'),
]

