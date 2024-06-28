from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
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


class AccountPasswordResetProfile(models.Model):
    account = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name="ResetPassword")
    reset_password_otp = models.IntegerField(
        null=True, default=None, blank=True)
    reset_password_expire = models.DateTimeField(null=True, blank=True)


@receiver(post_save, sender=get_user_model())
def make_reset_password_profile(sender, instance, created, **kwargs):
    account = instance
    if created:
        profile = AccountPasswordResetProfile(account=account)
        profile.save()
