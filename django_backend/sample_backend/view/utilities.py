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


def codec_check(request):
    if request.method == 'POST':
        codecs = []
        if (last_index := int(request.data['file_index'])) != -1:
            for i in range(last_index + 1):
                file = request.data[f'{i}']
                file_name = file.name
                file_obj = file
                new_video_media = VideoMedia(
                        created_at = timezone.now(),
                        name = file_name,
                        extension = 'unknown',
                        archive = file,
                        )
                new_video_media.save()

                video_url = os.path.join(settings.MEDIA_ROOT, new_video_media.archive.__str__())
                
                try:
                    sub = subprocess.Popen(
                        f"python3 ./sample_backend/VideoProcessors/codeccheck.py '{video_url}'",
                        text = True,
                        shell = True,
                        stdout = subprocess.PIPE,
                        universal_newlines=True
                    )

                    codecs.append(sub.stdout.read().split('\n')[0])
                except:
                    print("Error occurred in codec checking")
                
                if os.path.exists(video_url):
                    os.remove(video_url)
                    print(f"{video_url} file removed successfully")

                new_video_media.delete()

            print(codecs)
        return Response({'message': 'codec checking done', 'data': codecs.__repr__()})
    return Response({'message': 'wrong method call'})
