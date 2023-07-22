"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from django.contrib import admin
from .views import (delete_comment, delete_product, HomepageView, PostProduct, product_detail,
     ProductEditView)

app_name = "products"
urlpatterns = [
    path("", HomepageView.as_view(), name="homepage"),
    path("postproduct/", PostProduct.as_view(), name="postproduct"),
    path("products/<int:pk>/", product_detail, name="productdetail"),
    path("editproducts/<int:pk>/", ProductEditView.as_view(), name="editproduct"),
    path(
        "delete_comment/<int:comment_id>/",
        delete_comment,
        name="delete_comment",
    ),
    # path("deleteproduct/<int:pk>/", ProductDeleteView.as_view(), name="deleteproduct"),
    path("deleteproduct/<int:pk>/", delete_product, name="deleteproduct"),
    
    # path("check/", check_spam, name="check"),
]
