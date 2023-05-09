from django.urls import path
from .views import (
    CheckoutView,
    payment_cancelled,
    payment_successful,
    PaymentHistoryView,
    product_page,
    stripe_webhook,
)


app_name = "payment"
urlpatterns = [
    # path("checkout/<int:product_id>/", CheckoutView.as_view(), name="checkout"),
    path("checkout/<int:product_id>/", product_page, name="checkout"),
    path("product_page/", product_page, name="product_page"),
    path("payment_successful/", payment_successful, name="payment_successful"),
    path("payment_cancelled/", payment_cancelled, name="payment_cancelled"),
    path("stripe_webhook/   ", stripe_webhook, name="stripe_webhook"),
    path("payment_history/", PaymentHistoryView.as_view(), name="payment_history"),
]
