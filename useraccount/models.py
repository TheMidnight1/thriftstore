from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    image = models.ImageField(
        upload_to="images/",
        blank=True,
        null=True,
        default="images/default.jpg",
        
    )
    is_admin = models.BooleanField(default=False),
    is_user = models.BooleanField(default=True)
