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

def single_user(request):
    if request.method == "GET":
        try :
            _, token = request.META.get('HTTP_AUTHORIZATION').split(' ')
            user = get_user_from_token(token)
            return Response({
                'user': UserSerializer(user).data,
                'recent_visit': timezone.now()
            })
        except:
            return Response({"message": "No User with given credential exists"},
                status = status.HTTP_404_NOT_FOUND)
    return Response({"message": "wrong method call"},
        stauts = status.HTTP_405_METHOD_NOT_ALLOWED)

