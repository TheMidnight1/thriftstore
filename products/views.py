import django.contrib
import stripe
import json
from django.db.models import Q

from django.views import View
from .forms import CommentForm
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from .models import Product, Comment
from django.http import JsonResponse
from django.urls import reverse_lazy
from categories.models import Category
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView


# class HomepageView(ListView):
#     model = Product
#     template_name = "homepage.html"
#     context_object_name = "products"

#     def get_queryset(self):
#         if not self.request.user.is_authenticated:
#             # Return all products if user is not logged in
#             queryset = super().get_queryset()
#         else:
#             # Exclude products posted by the current user
#             queryset = super().get_queryset().exclude(user=self.request.user)
#         print("Current User:", self.request.user)
#         print("All Products:", super().get_queryset())
#         print("Filtered Products:", queryset)
#         return queryset


class HomepageView(ListView):
    model = Product
    template_name = "homepage.html"
    context_object_name = "products"

    def get_queryset(self):
        queryset = super().get_queryset()

        search_term = self.request.GET.get("search_term", "")
        if search_term:
            queryset = queryset.filter(name__icontains=search_term)

        if not self.request.user.is_authenticated:
            # Return all products if user is not logged in
            return queryset
        else:
            # Exclude products posted by the current user
            return queryset.exclude(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_term = self.request.GET.get("search_term", "")
        context["search_term"] = search_term
        return context


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


from .forms import CommentForm


# class ProductDetailView(LoginRequiredMixin, DetailView):
#     model = Product
#     template_name = "product_detail.html"
#     context_object_name = "product"


@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    comment_form = CommentForm(request.POST or None, initial={"product_id": product.pk})
    if request.method == "POST" and comment_form.is_valid():
        # Create a new Comment object
        comment = Comment(
            product=product,
            user=request.user,
            content=comment_form.cleaned_data["content"],
        )

        comment.save()
        messages.success(request, "Comment posted")
        comment_form = CommentForm()

        # Redirect to a success page or perform any other actions
    return render(
        request,
        "product_detail.html",
        {"product": product, "comment_form": comment_form},
    )


class ProductEditView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = "edit_product.html"
    fields = [
        "condition",
        "category",
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


# DELETE COMMENT


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Check if the logged-in user is the owner of the comment
    if comment.user == request.user:
        comment.delete()

    # Redirect to the product detail page or any other desired page
    return redirect("/")


# EDIT COMMENT
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == "POST":
        edit_form = CommentForm(request.POST)
        if edit_form.is_valid():
            comment.content = form.cleaned_data["content"]
            comment.save()
            return redirect("productdetail", pk=comment.product.pk)
    else:
        form = CommentForm(
            initial={"content": comment.content, "comment_id": comment_id}
        )

    return render(
        request, "product_detail.html", {"edit_form": edit_form, "comment": comment}
    )


def sidebar(request):
    categories = Category.objects.all()
    context = {"categories": categories}
    return render(request, "sidebar.html", context)


# def search_products(request):
#     search_term = request.GET.get("search_term", "")
#     search_products = Product.objects.filter(name__icontains=search_term)
#     return render(request, "homepage.html", {"search_products": search_products})
