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
from .utilities import get_user_from_token

def get_user_from_token(token):
    objs = AuthToken.objects.filter(token_key=token[:CONSTANTS.TOKEN_KEY_LENGTH])
    if len(objs) == 0:
        return None
    return objs.first().user

def create_user(request):
    if request.method == 'POST':
        client_ip = request.META.get("REMOTE_ADDR")
        if (len(request.data['username']) < 6) or (len(request.data['password']) < 6):
            message = {'message': "short field"}
            return Response(message, status = status.HTTP_400_BAD_REQUEST)
            
        serializer = CreateUserSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.save()
        user.client_ip = client_ip
        user.save()

        result = AuthorityRequest.objects.open_request(
            user = user,
            title = "회원가입 요청",
            comments = "화원가입 요청 드립니다",
            auth_from = 0,
            auth_to = int(request.data['authority'])
        )

        print(result)

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

def logout_user(request):
    _, token = request.META.get('HTTP_AUTHORIZATION').split(' ')
    if request.method == 'POST':
        try:
            user = get_user_from_token(token)
            print(user)
            user.auth_token_set.all().delete()
            return Response({"message": "User logged out"},
                status = status.HTTP_200_OK)
        except:
            return Response({"message": "Token removal error"},
                status = status.HTTP_404_NOT_FOUND)
