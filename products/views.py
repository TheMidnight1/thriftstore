from django.shortcuts import render
from django.views.generic import ListView
from .models import Product


class HomepageView(ListView):
    model = Product
    template_name = "homepage.html"
    context_object_name = "products"
