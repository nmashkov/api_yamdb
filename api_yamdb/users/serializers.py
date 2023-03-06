from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.utils import create_confirmation_code


User = get_user_model()


class UserSignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email')
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email'],
                message='На один email может быть зарегистрирован один '
                        + 'пользователь.'
            )
        ]

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                'Недопустимое имя пользователя.')
        return username

    def create(self, validated_data):
        """Create and return a new user."""

        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            confirmation_code=create_confirmation_code()
        )
        user.save()
        return user


class UserRecieveTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
        read_only_fields = ('username', 'confirmation_code',)
