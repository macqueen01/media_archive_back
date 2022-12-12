from json import JSONEncoder
import json
from rest_framework.response import Response
from rest_framework import status


from converter import Converter
from django.conf import settings
from sample_backend.model.abstractModels import CaseManager

from sample_backend.models import *
from sample_backend.serializer import *
from .utilities import get_user_from_token
from django.utils import timezone


def count_cases(request):
    if request.method == 'GET':
        img_count = ImageCase.objects.count_total_cases(False)
        vid_count = VideoCase.objects.count_total_cases(False)
        doc_count = DocCase.objects.count_total_cases(False)

        total = img_count + vid_count + doc_count

        return Response({
            'img': img_count,
            'vid' : vid_count,
            'doc' : doc_count,
            'total': total
        }, status = status.HTTP_200_OK)
    return Response({"message": "wrong method call"}, 
        status = status.HTTP_405_METHOD_NOT_ALLOWED)
