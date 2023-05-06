import time
import stripe
from .models import UserPayment
from django.conf import settings
from products.models import Product
from django.shortcuts import render
from django.views.generic import ListView
from django.http import Http404, HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class CheckoutView(TemplateView):
    model = Product
    template_name = "checkout.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs.get("product_id")
        context["product"] = get_object_or_404(Product, id=product_id)
        return context


@login_required(login_url="login")
def product_page(request, product_id):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST

    try:
        product = Product.objects.get(id=product_id)

    except Product.DoesNotExist:
        raise Http404("Product does not exist")

    if request.method == "POST":
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": int(product.price * 100),
                        "product_data": {
                            "name": product.name,
                            "description": product.description,
                        },
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            customer_creation="always",
            success_url=settings.REDIRECT_DOMAIN
            + f"/payment_successful?session_id={{CHECKOUT_SESSION_ID}}&product_id={product.id}",
            cancel_url=settings.REDIRECT_DOMAIN + "/payment_cancelled",
        )
        return redirect(checkout_session.url, code=303)

    return render(request, "checkout.html", {"product": product})


## use Stripe dummy card: 4242 4242 4242 4242
# def payment_successful(request):
#     stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
#     checkout_session_id = request.GET.get("session_id", None)
#     session = stripe.checkout.Session.retrieve(checkout_session_id)
#     customer = stripe.Customer.retrieve(session.customer)
#     user_payment = UserPayment(
#         user=request.user, checkout_id=checkout_session_id, is_successful=True
#     )
#     user_payment.save()
#     return render(request, "payment_successful.html", {"customer": customer})


@login_required
def payment_successful(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    checkout_session_id = request.GET.get("session_id", None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    customer = stripe.Customer.retrieve(session.customer)
    user_payment = UserPayment(
        user=request.user, checkout_id=checkout_session_id, is_successful=True
    )
    user_payment.save()
    payment_history = UserPayment.objects.filter(user=request.user)
    return render(
        request,
        "payment_successful.html",
        {"customer": customer, "payment_history": payment_history},
    )


def payment_cancelled(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    return render(request, "payment_cancelled.html")


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
    payload = request.body
    signature_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, signature_header, settings.STRIPE_WEBHOOK_SECRET_TEST
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        session_id = session.get("id", None)
        user_payment = UserPayment.objects.get(checkout_id=session_id)
        user_payment.is_successful = True
        user_payment.save()
    return HttpResponse(status=200)


class PaymentHistoryView(LoginRequiredMixin, ListView):
    model = UserPayment
    template_name = "payment_history.html"
    context_object_name = "payment_history"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user).order_by("-created_at")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        payment_history = self.get_queryset()
        payment_details = []
        for payment in payment_history:
            products = payment.products.all()
            product_details = []
            for product in products:
                seller_name = product.seller.username
                product_details.append((product, seller_name))
            payment_details.append((payment, product_details))
        context["payment_details"] = payment_details
        return context
