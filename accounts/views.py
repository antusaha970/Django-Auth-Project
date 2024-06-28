from random import randint
from django.shortcuts import render
from rest_framework.decorators import APIView
from .models import Account
from .serializers import AccountSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password


class AccountView(APIView):
    def get_permissions(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH' or self.request.method == "GET" or self.request.method == "DELETE":
            return [IsAuthenticated()]
        return [AllowAny()]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = AccountSerializer(data=data, many=False)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            response_data = {
                'user': serializer.data,
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh)
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        serializer = AccountSerializer(
            instance=user, data=data, many=False, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        serializer = AccountSerializer(
            instance=user, data=data, many=False, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = AccountSerializer(user)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response({"details": "Account deleted"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def login_account(request):
    data = request.data
    email = data.get('email', None)
    password = data.get('password', None)

    if email is None or password is None:
        return Response({"errors": "Email and password is required"}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, email=email, password=password)
    if user is not None:
        serializer = AccountSerializer(user, many=False)
        refresh = RefreshToken.for_user(user)
        response_data = {
            'user': serializer.data,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }
        return Response(response_data)

    return Response({'errors': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class ResetPasswordView(APIView):

    def get(self, request, *args, **kwargs):
        email = request.GET.get('email', None)
        if email is None:
            return Response({"errors": "Please pass email as query parameter"}, status=status.HTTP_400_BAD_REQUEST)

        account = get_object_or_404(Account, email=email)

        otp = randint(100000, 999999)+account.id
        expire_time = datetime.now()+timedelta(minutes=30)

        account.ResetPassword.reset_password_otp = otp
        account.ResetPassword.reset_password_expire = expire_time

        account.ResetPassword.save()

        message = f"Your password reset OTP is {otp}. It will expire in 30 Minutes"

        send_mail("Password reset OTP", message, "noreply@gmail.com", [email])

        return Response({"details": "Password reset OTP has been sent to {email}"})

    def post(self, request):
        OTP = request.data.get('OTP', None)
        password = request.data.get('password', None)
        confirm_password = request.data.get('confirm_password', None)
        if OTP is None or password is None or confirm_password is None:
            return Response({"errors": "OTP,Password,Confirm Password is required"}, status=status.HTTP_400_BAD_REQUEST)
        if password != confirm_password:
            return Response({"errors": "Passwords didn't match"}, status=status.HTTP_400_BAD_REQUEST)

        account = get_object_or_404(
            Account, ResetPassword__reset_password_otp=OTP)

        if account.ResetPassword.reset_password_expire.replace(tzinfo=None) < datetime.now():
            return Response({"errors": "Invalid OTP"}, status=status.HTTP_403_FORBIDDEN)

        account.password = make_password(password)
        account.save()
        account.ResetPassword.reset_password_otp = None
        account.ResetPassword.reset_password_expire = None
        account.ResetPassword.save()

        return Response({"details": "password reset successful"})
