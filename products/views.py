import stripe
from .models import Product
from django.views import View
from django.urls import reverse
from django.conf import settings
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView


class HomepageView(ListView):
    model = Product
    template_name = "homepage.html"
    context_object_name = "products"

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            # Return all products if user is not logged in
            queryset = super().get_queryset()
        else:
            # Exclude products posted by the current user
            queryset = super().get_queryset().exclude(user=self.request.user)
        print("Current User:", self.request.user)
        print("All Products:", super().get_queryset())
        print("Filtered Products:", queryset)
        return queryset


class PostProduct(LoginRequiredMixin, CreateView):
    model = Product
    fields = [
        "category",
        "condition",
        "name",
        "brand",
        "description",
        "price",
        "manufactured_date",
        "product_image",
    ]
    success_url = reverse_lazy("products:homepage")
    template_name = "post_products.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"


class ProductEditView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = "edit_product.html"
    fields = [
        "name",
        "brand",
        "description",
        "price",
        "manufactured_date",
        "product_image",
    ]
    success_url = reverse_lazy("useraccount:userprofile")


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "user_profile.html"
    success_url = reverse_lazy("useraccount:userprofile")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = reverse_lazy("useraccount:userprofile")

        self.object.delete()
        return redirect(success_url)


class CheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    "price": "{{PRICE_ID}}",
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url=request.build_absolute_uri(reverse("success")),
            cancel_url=request.build_absolute_uri(reverse("cancel")),
        )
        return JsonResponse({"id": checkout_session.id})
