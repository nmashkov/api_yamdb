from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class UserSignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254)
    username = serializers.RegexField(regex=r'^[a-zA-Z][a-zA-Z0-9-_.]{1,20}$',
                                      max_length=150)

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                'Недопустимое имя пользователя.')
        return username


class UserRecieveTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
        read_only_fields = ('username', 'confirmation_code',)

    def validate_username(self, username):
        if len(username) > 150:
            raise serializers.ValidationError(
                'Имя пользователя должно быть меньше 151 символа.')
        return username


class UsersSerializer(serializers.ModelSerializer):
    role = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')
