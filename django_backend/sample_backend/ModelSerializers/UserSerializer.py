from rest_framework import serializers
from sample_backend.models import *
from django.contrib.auth import authenticate

from .CaseSerializer import *

class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "username",
            "position",
            "standing",
            "name",
            "password",
            "affiliation"
        )

        extra_kwargs = {'password': {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "username",
            "id",
            "position",
            "standing",
            "name",
            "affiliation"
        )

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to login with provided credentials")

