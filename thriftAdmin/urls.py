from django.urls import path
from .views import admin_login, admin_homepage

app_name = "thriftAdmin"

urlpatterns = [
    path("admin_login/", admin_login.as_view(), name="admin_login"),
    path("admin_homepage/", admin_homepage, name="admin_homepage"),
]
