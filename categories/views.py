from django.shortcuts import render
from .models import Category, Condition
from products.models import Product


def category_products(request, category_id):
    category = Category.objects.get(id=category_id)
    products = Product.objects.filter(category=category)
    context = {"category": category, "products": products}
    return render(request, "category_products.html", context)


def condition_products(request, condition_id):
    condition = Condition.objects.get(id=condition_id)
    products = Product.objects.filter(condition=condition)
    context = {"condition": condition, "products": products}
    return render(request, "condition_products.html", context)
