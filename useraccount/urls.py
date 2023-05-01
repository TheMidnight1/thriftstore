from django.urls import path
from .views import MyLoginView, MyRegisterView, Logout

app_name = "useraccount"
urlpatterns = [
    path("register/", MyRegisterView.as_view(), name="register"),
    path("login/", MyLoginView.as_view(), name="login"),
    path("logout/", Logout.as_view(), name="logout"),
]
