from django.urls import path
from .views import category_products, condition_products, FilteredProductsView

app_name = "categories"
urlpatterns = [
    path("category/<int:category_id>/", category_products, name="category_products"),
    path(
        "condition/<int:condition_id>/", condition_products, name="condition_products"
    ),
    path(
        "filtered-products/", FilteredProductsView.as_view(), name="filtered_products"
    ),
]
