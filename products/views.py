import json
import torch
import stripe
import time

import numpy as np
from PIL import Image
from django.views import View
from .forms import CommentForm,ReviewForm
from django.urls import reverse
from django.db.models import Q
from payment.models import UserPayment
from django.conf import settings
from django.contrib import messages
from .models import FeatureVector, Product
from django.http import JsonResponse
from .models import Product, Comment
from django.http import JsonResponse
from django.urls import reverse_lazy
from categories.models import Category
from django.views.generic import ListView
import torchvision.transforms as transforms
from sklearn.metrics.pairwise import cosine_similarity
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic.edit import CreateView, UpdateView, DeleteView


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

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.save()
            create_feature_vectors()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

@login_required
def product_detail(request, pk):
    start_time = time.time()

    product = get_object_or_404(Product, pk=pk)
    has_payment = UserPayment.objects.filter(user=request.user, products=product).exists()
    test_product = product
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
        
    #Review 
    if request.method == 'POST' and has_payment:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', pk=pk)
    else:
        form = ReviewForm()

    # Calculate similarity and recommend similar products
    def recommend_similar_products(clicked_product_id, top_n=4):
        clicked_product = test_product
        clicked_product_feature_vector = FeatureVector.objects.get(
            product=clicked_product
        )
        clicked_product_feature_vector_list = json.loads(
            clicked_product_feature_vector.feature_vector
        )
        clicked_product_feature_vector_array = np.array(
            clicked_product_feature_vector_list
        )

        # Retrieve all products except the clicked product
        # all_products = Product.objects.exclude(id=clicked_product_id)
        all_products = Product.objects.filter(category=clicked_product.category).exclude(id=clicked_product_id)


        # Calculate similarity scores for each product
        similarity_scores = []
        for product in all_products:
            product_feature_vector = FeatureVector.objects.get(product=product)
            product_feature_vector_list = json.loads(
                product_feature_vector.feature_vector
            )
            product_feature_vector_array = np.array(product_feature_vector_list)

            similarity = cosine_similarity(
                [clicked_product_feature_vector_array],
                [product_feature_vector_array],
            )[0][0]

            similarity_scores.append((product, similarity))

        # Sort products based on similarity scores in descending order
        similarity_scores.sort(key=lambda x: x[1], reverse=True)

        # Select the top N products with the highest similarity scores as recommendations
        top_similar_products = [product for product, _ in similarity_scores[:top_n]]

        return top_similar_products

    # Recommend similar products
    similar_products = recommend_similar_products(pk)
    elapsed_time = time.time() - start_time
    print(elapsed_time)
    context = {
        "product": product,
        "comment_form": comment_form,
        "similar_products": similar_products,
        'form': form, 
        'has_payment': has_payment
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


# THIS IS THE CODE TO EXTRACT EXISITING PRODUCT FEATURES


def extract_features_from_image(image_path):
    # Load the image and apply necessary transformations
    image = Image.open(image_path).convert("RGB")
    transform = transforms.Compose(
        [
            transforms.Resize((224,224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )
    image = transform(image).unsqueeze(0)

    # Load the pre-trained model
    model = torch.hub.load("pytorch/vision", "resnet18", pretrained=True)
    model.eval()

    # Extract the features
    with torch.no_grad():
        features = model(image).squeeze().numpy().tolist()

    return features


# Code to extract features for existing products and store them in FeatureVector
def create_feature_vectors():
    # Retrieve all products
    products = Product.objects.all()

    # Iterate over the products
    for product in products:
        # Check if feature vector already exists for the product
        if FeatureVector.objects.filter(product=product).exists():
            continue  # Skip if feature vector already exists

        # Extract features from the image
        feature_vector = extract_features_from_image(product.product_image.path)

        # Create a new FeatureVector object
        feature_vector_obj, created = FeatureVector.objects.get_or_create(
            product=product, defaults={"feature_vector": json.dumps(feature_vector)}
        )

        # Save the FeatureVector object
        feature_vector_obj.save()


# Call the create_feature_vectors function to extract features for existing products
create_feature_vectors()
