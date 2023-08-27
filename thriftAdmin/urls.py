from django.urls import path
from .views import (admin_login, admin_homepage,manage_products,manage_condition,
manage_users,manage_categories ,edit_condition,add_condition,add_category,delete_category,edit_category,delete_product,delete_user)

app_name = "thriftAdmin"

urlpatterns = [
    path("admin_login/", admin_login.as_view(), name="admin_login"),
    path("admin_homepage/", admin_homepage, name="admin_homepage"),
    path('products/',manage_products,name="products"),
    path('deleteproduct/<int:pk>',delete_product,name="deleteproduct"),
    
    
    path('conditions/',manage_condition,name="conditions"),
    path('addconditions/',add_condition,name="addconditions"),
    path('editcondition/<int:pk>',edit_condition,name="editcondition"),
    
    
    path('users/',manage_users,name="users"),
    path('deleteuser=/<int:pk>',delete_user,name="deleteuser"),
    
    
    path('categories/',manage_categories,name="categories"),
    path('addcategory/',add_category,name="addcategory"),
    path('deletecategory/<int:pk>',delete_category,name="deletecategory"),
    path('editcategory/<int:pk>',edit_category,name="editcategory"),
    
    
    
    
]
