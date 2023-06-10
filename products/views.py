import stripe
from django import forms
from django.db.models import Q
from django.views import View
from .forms import CommentForm
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
from .models import Product, Comment
from django.http import JsonResponse
from django.urls import reverse_lazy
from categories.models import Category
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.conf import settings
from .forms import CommentForm

import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


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


# def extract_image_features(image_path):
#     # Load the image
#     image = Image.open(image_path).convert("RGB")

#     # Preprocess the image
#     preprocessed_image = preprocess_input(
#         tf.expand_dims(np.array(image.resize((224, 224))), axis=0)
#     )

#     # Load the pretrained ResNet model
#     base_model = ResNet50(weights="imagenet", include_top=False, pooling="avg")

#     # Create a new model with the base model's output as the output layer
#     model = Model(inputs=base_model.input, outputs=base_model.output)

#     # Pass the preprocessed image through the model to obtain the feature vector
#     features = model.predict(preprocessed_image)

#     # Return the feature vector representation
#     return features


class HomepageView(ListView):
    model = Product
    template_name = "homepage.html"
    context_object_name = "products"
    paginate_by = settings.DEFAULT_PAGINATION_SIZE

    def get_queryset(self):
        queryset = super().get_queryset()

        search_term = self.request.GET.get("search_term", "")
        if search_term:
            queryset = queryset.filter(name__icontains=search_term)

        if not self.request.user.is_authenticated:
            return queryset.order_by("?")  # Randomly order the products
        else:
            return queryset.exclude(user=self.request.user).order_by("?")

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
        "quantity",
    ]
    success_url = reverse_lazy("products:homepage")
    template_name = "post_products.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    # @login_required
    # def product_detail(request, pk):
    # product = get_object_or_404(Product, pk=pk)
    # comment_form = CommentForm(request.POST or None, initial={"product_id": product.pk})
    # if request.method == "POST" and comment_form.is_valid():
    #     # Create a new Comment object
    #     comment = Comment(
    #         product=product,
    #         user=request.user,
    #         content=comment_form.cleaned_data["content"],
    #     )

    #     comment.save()
    #     messages.success(request, "Comment posted")
    #     comment_form = CommentForm()

    #     # Redirect to a success page or perform any other actions
    # return render(
    #     request,
    #     "product_detail.html",
    #     {"product": product, "comment_form": comment_form},
    # )


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

    # Retrieve the clicked product details from the database
    def get_clicked_product_details(product_id):
        product = get_object_or_404(Product, id=product_id)
        # Retrieve relevant details of the clicked product
        return product

    # Extract features from the clicked product's image
    def extract_features_from_image(image):
        # Preprocess the image (resize, normalize, etc.) to match the model's input requirements
        preprocess = transforms.Compose(
            [
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
                ),
            ]
        )
        image = preprocess(image)
        image = image.unsqueeze(0)
        # Pass the preprocessed image through the feature extraction layer of your pretrained model
        feature_vector = model(image)
        feature_vector = feature_vector.detach().numpy()
        return feature_vector

    # Calculate similarity and recommend similar products
    def recommend_similar_products(clicked_product_id, top_n=4):
        clicked_product = get_clicked_product_details(clicked_product_id)
        clicked_product_image = Image.open(clicked_product.product_image.path).convert(
            "RGB"
        )
        clicked_product_features = extract_features_from_image(clicked_product_image)

        # Retrieve all products except the clicked product
        all_products = Product.objects.exclude(id=clicked_product_id)

        # Calculate similarity scores for each product
        similarity_scores = []
        for product in all_products:
            product_image = Image.open(product.product_image.path).convert("RGB")
            product_features = extract_features_from_image(product_image)

            # Reshape the feature vectors to 2D arrays
            clicked_product_features_2d = clicked_product_features.reshape(1, -1)
            product_features_2d = product_features.reshape(1, -1)

            # Calculate similarity using cosine similarity or other appropriate metric
            similarity = cosine_similarity(
                clicked_product_features_2d, product_features_2d
            )[0][0]
            similarity_scores.append((product, similarity))

        # Sort products based on similarity scores in descending order
        similarity_scores.sort(key=lambda x: x[1], reverse=True)

        # Select the top N products with the highest similarity scores as recommendations
        top_similar_products = [product for product, _ in similarity_scores[:top_n]]

        return top_similar_products

    # PyTorch model initialization
    model = models.vgg16(pretrained=True)
    model = model.features
    model.eval()

    # Recommend similar products
    similar_products = recommend_similar_products(pk)

    context = {
        "product": product,
        "comment_form": comment_form,
        "similar_products": similar_products,
    }

    return render(request, "product_detail.html", context)


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
        "quantity",
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
