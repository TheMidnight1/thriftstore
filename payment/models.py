import django.conf
from django.db import models
from useraccount.models import User
from products.models import Product
from django.dispatch import receiver
from django.conf import settings

from django.db.models.signals import post_save


class UserPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    checkout_id = models.CharField(max_length=500)
    is_successful = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product)

    # class UserPayment(models.Model):
    #     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #     checkout_id = models.CharField(max_length=255)
    #     is_successful = models.BooleanField(default=False)
    #     seller_name = models.CharField(max_length=255)
    #     product_name = models.CharField(max_length=255)
    #     product_image = models.ImageField(upload_to="product_images", blank=True, null=True)
    #     product_price = models.DecimalField(max_digits=6, decimal_places=2)
    #     created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.checkout_id}"

    @receiver(post_save, sender=User)
    def create_user_payment(sender, instance, created, **kwargs):
        if created:
            UserPayment.objects.create(user=instance)
