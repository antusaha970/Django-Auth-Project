from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
# Create your models here.


class Account(AbstractUser):
    username = None
    phone_number = models.CharField(max_length=12, default=None, null=True)
    profile_picture = models.ImageField(
        upload_to="profile", default="profile.jgp")
    bio = models.CharField(max_length=255, default="", blank=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self) -> str:
        return self.email
