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
from knox.models import AuthToken

import os
import subprocess

from sample_backend.models import *
from django.utils import timezone
from knox.settings import CONSTANTS


def codec_check(request):
    if request.method == 'POST':
        codecs = []
        last_index = int(request.data['file_index'])
        if last_index != -1:
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


def get_user_from_token(token):
    objs = AuthToken.objects.filter(token_key=token[:CONSTANTS.TOKEN_KEY_LENGTH])
    if len(objs) == 0:
        return None
    return objs.first().user


def check_user_level(user):
    if user.is_staff and user.is_active:
        return 2
    elif not user.is_staff and user.is_active:
        return 1
    elif not user.is_staff and not user.is_active:
        return 0
    elif user.is_staff:
        # level of an inactive admin is still 2
        return 2
    else:
        return False

def case_id_map_parser(request):
    image_cases = request.data['image_cases']
    video_cases = request.data['video_cases']
    doc_cases = request.data['doc_cases']

    # construction 

    case_id_map = {}

    if image_cases:
        case_id_map[0] = image_cases
    if video_cases:
        case_id_map[1] = video_cases
    if doc_cases:
        case_id_map[2] = doc_cases

    return case_id_map

def authority_check(case, user):
    case_form = case.form
    if case_form == 0:
        user_lst = case.form0_accessed_by.all()
    elif case_form == 1:
        user_lst = case.form1_accessed_by.all()
    elif case_form == 2:
        user_lst = case.form2_accessed_by.all()
    else:
        return False
    
    if (user in user_lst) or (user.is_staff):
        return True