from rest_framework import serializers
from .models import User, Case

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CaseUploadSerializer(serializers.ModelSerializer):
    src = serializers.ImageField(use_url=True)

    class Meta:
        model = Case
        fields = '__all__'

