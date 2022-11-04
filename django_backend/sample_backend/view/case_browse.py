from json import JSONEncoder
import json
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import exceptions
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

        browse_cases = case_obj.objects.all().order_by('-created_at')

        paginator = PageNumberPagination()
        paginator.page_size = 12
        result_page = paginator.paginate_queryset(browse_cases, request)
        serializer = serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    return Response({'message': "wrong method call"})


def detail(request, form, id):
    form = form
    key = id 
    if request.method == 'GET':
        try:
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
                return Response({'message': 'The file type requested cannot be browsed', 'code': 0})
            
            if (not browse_object.exists()):
                return Response({'message': 'The file with given id does not exist', 'code': 0})
            else:
                result = serializer(browse_object.get())
                return Response(result.data)

        except:
            return Response({'message': 'The file type has not submitted', 'code': 0})