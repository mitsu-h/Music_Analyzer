from rest_framework import serializers
from dj_rest_auth.registration.serializers import (
    RegisterSerializer as DefaultRegisterSerializer,
)
from dj_rest_auth.serializers import UserDetailsSerializer
from allauth.utils import email_address_exists, get_username_max_length

from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password")

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"], password=validated_data["password"]
        )
        return user
