from django.urls import path
from rest_framework_simplejwt.views import (TokenRefreshView)

from legalUser.API.views import (
    UserCreateAV, 
    UserListAV,
    UserDetailAV,
    UserLoginAV,
    OTPVerifyAV,
    OTPCreateAV,
    AdminUserCreateAV
    )

urlpatterns = [
    
    # user paths
    path('createuser',UserCreateAV.as_view(), name="CreateUser"),
    path("listusers",UserListAV.as_view(), name="ListUsers"),
    path("getuserbyid/<uuid:pk>", UserDetailAV.as_view(),name="UserDetails"),
    path("login", UserLoginAV.as_view(), name="Login"),
    path("refreshtoken", TokenRefreshView.as_view(), name="RefreshToken"),

    # admin paths
    path("createadmin", AdminUserCreateAV.as_view(), name="CreateAdmin"),
    
    #otp paths
    path("verifyotp", OTPVerifyAV.as_view(), name="VerifyOtp"),
    path("createotp", OTPCreateAV.as_view(), name="CreateOTP")
]