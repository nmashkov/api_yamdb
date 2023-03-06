from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import status, permissions, exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.tokens import AccessToken

from users.serializers import (
    UserSignupSerializer,
    UserRecieveTokenSerializer
)


User = get_user_model()


class APIUserSignup(APIView):
    permission_classes = [permissions.AllowAny,]

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = get_object_or_404(User, username=request.data['username'])
            confirmation_code = user.confirmation_code
            user.email_user(
                'Confirmation code',
                f'{confirmation_code}',
                from_email='yamdb@ya.ru'
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenViewBase(TokenViewBase):
    permission_classes = [permissions.AllowAny,]

    def post(self, request):
        serializer = UserRecieveTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')
        if (username is None) or (confirmation_code is None):
            raise exceptions.AuthenticationFailed(
                'Необходимы username и код подтверждения.')
        user = User.objects.filter(username=username).first()
        if user is None:
            raise exceptions.AuthenticationFailed('Пользователь не найден.')
        if confirmation_code != str(user.confirmation_code):
            raise exceptions.AuthenticationFailed(
                'Неверный код подтверждения.')
        token = AccessToken.for_user(user)
        return Response({"token": f'{token}'}, status=status.HTTP_200_OK)
