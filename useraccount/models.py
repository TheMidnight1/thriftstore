from django.db import models
from django.contrib.auth.models import AbstractUser


# CREATE A USER MODEL

# class User(models.Model):
#     username = models.CharField(max_length=100, unique=True)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=100)
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     date_of_birth = models.DateField(null=True, blank=True)
#     gender = models.CharField(max_length=10, null=True, blank=True)
#     phone_number = models.CharField(max_length=20, null=True, blank=True)
#     address = models.CharField(max_length=255,null=True, blank=True)
#     date_joined = models.DateTimeField(auto_now_add=True)


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    image = models.ImageField(upload_to="user_images", blank=True, null=True)
