from django.urls import path
from .views import admin_login, admin_homepage,manage_products,manage_condition,manage_users,manage_categories

app_name = "thriftAdmin"

urlpatterns = [
    path("admin_login/", admin_login.as_view(), name="admin_login"),
    path("admin_homepage/", admin_homepage, name="admin_homepage"),
    path('products/',manage_products,name="products"),
    path('conditions/',manage_condition,name="conditions"),
    path('users/',manage_users,name="users"),
    path('categories/',manage_categories,name="categories"),
    
]
