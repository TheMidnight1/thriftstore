from django.urls import path
from .views import (
    MyLoginView,
    MyRegisterView,
    Logout,
    UserProfile,
    EditProfileView,
    ChangePasswordView,
)

app_name = "useraccount"
urlpatterns = [
    path("logout/", Logout.as_view(), name="logout"),
    path("login/", MyLoginView.as_view(), name="login"),
    path("register/", MyRegisterView.as_view(), name="register"),
    path("userprofile/", UserProfile.as_view(), name="userprofile"),
    path("editprofile/", EditProfileView.as_view(), name="edit_profile"),
    path("changepassword/", ChangePasswordView.as_view(), name="changepassword"),
]
