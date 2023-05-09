from django.shortcuts import render
from django.views.generic import ListView
from categories.models import Category


def category_list(request):
    categories = Category.objects.all()
    return render(request, "side_bar.html", {"categories": categories})
