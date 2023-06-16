from django.shortcuts import render
from .models import Category, Condition
from products.models import Product
from django.views.generic import View
from decimal import Decimal, InvalidOperation


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


class FilteredProductsView(View):
    template_name = "filtered_products.html"

    def get(self, request):
        category_id = request.GET.get("category")
        condition_id = request.GET.get("condition")
        min_price = request.GET.get("min_price")
        max_price = request.GET.get("max_price")

        try:
            min_price = Decimal(min_price)
        except (TypeError, ValueError, InvalidOperation):
            min_price = None

        try:
            max_price = Decimal(max_price)
        except (TypeError, ValueError, InvalidOperation):
            max_price = None

        products = Product.objects.exclude(user=request.user)

        if category_id:
            products = products.filter(category_id=category_id)
        if condition_id:
            products = products.filter(condition_id=condition_id)
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)

        context = {"products": products}
        return render(request, self.template_name, context)
