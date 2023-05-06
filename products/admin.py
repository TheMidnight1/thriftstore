from django.contrib import admin
from django.forms import FileInput
from .models import Product
from django.db import models
from django.forms import ClearableFileInput


class ProductAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.BinaryField: {"widget": ClearableFileInput(attrs={"multiple": True})},
    }


admin.site.register(Product, ProductAdmin)
