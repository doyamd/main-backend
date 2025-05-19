from django.urls import path
from rest_framework_simplejwt.views import (TokenRefreshView)

from legalUser.API.views import (
    UserCreateAV, 
    UserListAV,
    UserDetailAV,
    UserLoginAV,
    OTPVerifyAV,
    OTPCreateAV,
    AdminUserCreateAV,
    AttorneyUploadLicenseAV,
    UserUploadImageAV,
    AttorneyListAV,
    ToggleAttorneyApprovalAV,
    AttorneyEducationExperienceListAV,
    AttorneyEducationExperienceCreateAV
    )

urlpatterns = [
    
    # user paths
    path('createuser',UserCreateAV.as_view(), name="CreateUser"),
    path("listusers",UserListAV.as_view(), name="ListUsers"),
    path("getuserbyid/<uuid:pk>", UserDetailAV.as_view(),name="UserDetails"),
    path("login", UserLoginAV.as_view(), name="Login"),
    path("refreshtoken", TokenRefreshView.as_view(), name="RefreshToken"),
    path("user/uploadimage", UserUploadImageAV.as_view(), name="UploadImage"),

    # attorney paths
    path("attorney/uploadlicense", AttorneyUploadLicenseAV.as_view(), name="UploadLicense"),
    path("attorney/list", AttorneyListAV.as_view(), name="ListAttorneys"),
    path("attorney/toggleapproval/<uuid:pk>", ToggleAttorneyApprovalAV.as_view(), name="ToggleAttorneyApproval"),
    path("attorney/educationandexperience/<uuid:pk>", AttorneyEducationExperienceListAV.as_view(), name="EducationAndExperience"),
    path("attorney/educationandexperience", AttorneyEducationExperienceCreateAV.as_view(), name="UpdateEducationAndExperience"),
    # admin paths
    path("createadmin", AdminUserCreateAV.as_view(), name="CreateAdmin"),
    
    #otp paths
    path("verifyotp", OTPVerifyAV.as_view(), name="VerifyOtp"),
    path("createotp", OTPCreateAV.as_view(), name="CreateOTP")
]