from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import status, permissions, viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.tokens import AccessToken

from users.utils import create_confirmation_code
from users.permissions import IsAdmin
from users.serializers import (
    UserSignupSerializer, UserRecieveTokenSerializer,
    UsersSerializer
)


User = get_user_model()


class APIUserSignup(APIView):
    '''
    Регистрация нового пользователя и повторная отправка кода подтверждения.
    Права доступа: Доступно без токена.
    '''
    permission_classes = [permissions.AllowAny,]

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.data.get('username')
        email = request.data.get('email')
        new_confirmation_code = create_confirmation_code()
        if User.objects.filter(username=username, email=email).exists():
            user = User.objects.filter(username=username, email=email).first()
            user.confirmation_code = new_confirmation_code
            user.save()
        elif User.objects.filter(username=username).exists():
            user = User.objects.filter(username=username).first()
            if str(user.email) != email:
                return Response('Пользователь с таким именем уже существует.',
                                status=status.HTTP_400_BAD_REQUEST)
        elif User.objects.filter(email=email).exists():
            user = User.objects.filter(email=email).first()
            if str(user.username) != username:
                return Response('Пользователь с такой почтой уже существует.',
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save(confirmation_code=new_confirmation_code)
        user = get_object_or_404(User, username=username)
        user.email_user(
            f'Confirmation code for {user.role} {user.username}',
            f'Confirmation code for {user.role} {user.username}: '
            f'{new_confirmation_code}',
            from_email='yamdb@ya.ru'
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomTokenViewBase(TokenViewBase):
    '''
    Получение JWT-токена.
    Права доступа: Доступно без токена.
    '''
    permission_classes = [permissions.AllowAny,]

    def post(self, request):
        serializer = UserRecieveTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')
        if not username or not confirmation_code:
            return Response('Необходимы username и код подтверждения.',
                            status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            user = User.objects.filter(username=username).first()
        else:
            return Response('Пользователь не найден.',
                            status=status.HTTP_404_NOT_FOUND)
        if confirmation_code != str(user.confirmation_code):
            return Response('Неверный код подтверждения.',
                            status=status.HTTP_400_BAD_REQUEST)
        token = AccessToken.for_user(user)
        return Response({"token": f'{token}'}, status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    '''
    Функция представления и регистрация пользователей.
    Права доступа: Администратор.
    '''
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    search_fields = ('username',)
    permission_classes = (IsAdmin,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.data.get('username')
        email = request.data.get('email')
        if User.objects.filter(username=username).exists():
            user = User.objects.filter(username=username).first()
            if str(user.email) != email:
                return Response('Пользователь с таким именем уже существует.',
                                status=status.HTTP_400_BAD_REQUEST)
        elif User.objects.filter(email=email).exists():
            user = User.objects.filter(email=email).first()
            if str(user.username) != username:
                return Response('Пользователь с такой почтой уже существует.',
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def perform_create(self, serializer):
        new_confirmation_code = create_confirmation_code()
        serializer.save(confirmation_code=new_confirmation_code)
        email = serializer.data.get('email')
        username = serializer.data.get('username')
        role = serializer.data.get('role')
        send_mail(
            f'Confirmation code for {role} {username}',
            f'Confirmation code for {role} {username}: '
            f'{new_confirmation_code}',
            'yamdb@ya.ru',
            [f'{email}']
        )
