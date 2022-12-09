from json import JSONEncoder
import json
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import exceptions, status
from rest_framework.pagination import PageNumberPagination
from drf_multiple_model.pagination import MultipleModelLimitOffsetPagination
from drf_multiple_model.views import FlatMultipleModelAPIView

from converter import Converter
from django.conf import settings

import os
import subprocess

from sample_backend.models import *
from sample_backend.serializer import *
from django.utils import timezone
from .utilities import get_user_from_token, authority_check


def main(request, form):
    if (request.method == 'GET'):
        if form == 0:
            case_obj = ImageCase
            serializer_class = ImageCaseSerializer
        elif form == 1:
            case_obj = VideoCase
            serializer_class = VideoCaseSerializer
        elif form == 2:
            case_obj = DocCase
            serializer_class = VideoCaseSerializer

        browse_cases = case_obj.objects.filter(uploaded__exact = 1).order_by('-created_at')

        paginator = PageNumberPagination()
        paginator.page_size = 12
        result_page = paginator.paginate_queryset(browse_cases, request)
        serializer = serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    return Response({'message': "wrong method call"}, 
        status = status.HTTP_405_METHOD_NOT_ALLOWED)


def detail(request, form, id):
    form = form
    key = id
    _, token = request.META.get('HTTP_AUTHORIZATION').split(' ')
    print(token)
    if request.method == 'GET':
        if (form == 0):
            browse_object = ImageCase.objects.filter(id__exact = key)
            serializer = ImageCaseSerializer
        elif (form == 1):
            browse_object = VideoCase.objects.filter(id__exact = key)
            serializer = VideoCaseSerializer
        elif (form == 2):
            browse_object = DocCase.objects.filter(id__exact = key)
            serializer = VideoCaseSerializer
        else:
            return Response({'message': 'The file type requested cannot be browsed'},
                status = status.HTTP_400_BAD_REQUEST)
        
        if (not browse_object.exists()):
            return Response({'message': 'The file with given id does not exist'},
                status = status.HTTP_410_GONE)
        
        if authority_check(browse_object.get(), get_user_from_token(token)):
            result = serializer(browse_object.get())
            return Response(result.data)

        return Response({'message': 'User has no authority to the case'},
            status = status.HTTP_401_UNAUTHORIZED)

    return Response({'message': "wrong method call"},
        status = status.HTTP_405_METHOD_NOT_ALLOWED)