from django.urls import path
from .views import AccountView, login_account, ResetPasswordView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView, TokenRefreshView

urlpatterns = [
    path('accounts/', AccountView.as_view()),
    path('accounts/reset-password/', ResetPasswordView.as_view()),
    path('accounts/login', login_account),
    path('accounts/obtain-token/', TokenObtainPairView.as_view()),
    path('accounts/verify-token/', TokenVerifyView.as_view()),
    path('accounts/refresh-token/', TokenRefreshView.as_view()),
]
