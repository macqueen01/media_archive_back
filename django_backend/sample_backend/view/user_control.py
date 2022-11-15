from json import JSONEncoder
import json
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions, status
from rest_framework.pagination import PageNumberPagination
from drf_multiple_model.pagination import MultipleModelLimitOffsetPagination
from drf_multiple_model.views import FlatMultipleModelAPIView
from knox.models import AuthToken
from knox.settings import CONSTANTS

from converter import Converter
from django.conf import settings

from sample_backend.models import *
from sample_backend.serializer import *
from django.utils import timezone
from knox.settings import CONSTANTS

def get_user_from_token(token):
    objs = AuthToken.objects.filter(token_key=token[:CONSTANTS.TOKEN_KEY_LENGTH])
    if len(objs) == 0:
        return None
    return objs.first().user

def create_user(request):
    if request.method == 'POST':
        if (len(request.data['username']) < 6) or (len(request.data['password']) < 6):
            message = {'message': "short field"}
            return Response(message, status = status.HTTP_400_BAD_REQUEST)
            
        serializer = CreateUserSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.save()

        return Response(
            {
                "user": UserSerializer(user).data,
                "token": AuthToken.objects.create(user)[1]
            }
        )
    return Response({'message': "wrong method call"}, status = status.HTTP_405_METHOD_NOT_ALLOWED)

def login_user(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data
        return Response(
            {
                'user': UserSerializer(user).data,
                'token': AuthToken.objects.create(user)[1]
            }
        )
    return Response({"message": "wrong method call on login"},
        status = status.HTTP_405_METHOD_NOT_ALLOWED)