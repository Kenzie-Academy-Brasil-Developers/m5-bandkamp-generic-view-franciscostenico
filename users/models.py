from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class User(AbstractUser):
    username = models.CharField(max_length=64, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    objects = UserManager()
