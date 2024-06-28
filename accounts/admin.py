from django.contrib import admin
from .models import Account, AccountPasswordResetProfile
# Register your models here.
admin.site.register(Account)
admin.site.register(AccountPasswordResetProfile)
