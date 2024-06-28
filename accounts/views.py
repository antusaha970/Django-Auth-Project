from django.shortcuts import render
from rest_framework.decorators import APIView
from .models import Account
from .serializers import AccountSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate


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
