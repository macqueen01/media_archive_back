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
from time import sleep
from django.conf import settings

import os
import subprocess

from .models import *
from .serializer import *
from django.utils import timezone

# Create your views here.

class UserListAPI(APIView):
    def get(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many = True)
        return Response(serializer.data)

class ResponseThen(Response):
    def __init__(self, data, then_callback, **kwargs):
        super().__init__(data, **kwargs)
        self.then_callback = then_callback

    def close(self):
        super().close()
        self.then_callback()



@api_view(['GET'])
def browse_view(request, form):
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

        browse_cases = case_obj.objects.all()

        paginator = PageNumberPagination()
        paginator.page_size = 12
        result_page = paginator.paginate_queryset(browse_cases, request)
        serializer = serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    return Response({'message': "wrong method call"})


class LimitPagination(MultipleModelLimitOffsetPagination):
    default_limit = 12

class BrowseCaseAPIView(FlatMultipleModelAPIView):
    pagination_class = LimitPagination
    add_model_type = True
    sorting_fields = ['created_at']

    def get_querylist(self):

        image_case_to_join = ImageCase.objects.all()
        video_case_to_join = VideoCase.objects.all()

        # un_sorted_queryset = activity_serializer.data + team_serializer.data + team_player_left_serializer.data

        querylist = (
            {'queryset': image_case_to_join.distinct(), 'serializer_class': ImageCaseSerializer},
            {'queryset': video_case_to_join.distinct(), 'serializer_class': VideoCaseSerializer},
        )

        return querylist


@api_view(['GET'])
def browse_detail(request, form, id):
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

@api_view(['GET','POST'])
def image_case_create_view(request):

    def do_after():
        # ...code to run *after* response is returned to client
        pass
    

    if request.method == 'POST':
        reference_list = []
        attendee = []
        title = request.data['title']
        content = request.data['content']
        private = request.data['private']
        produced = request.data['produced']
        file_format = request.data['type']
        
        # In case we relate Location, Personel, User to this obj
        # followings are the foreignKey items of ImageCase

        attendee_list = request.data['attendee'].split(',')
        associate = request.data['associate']
        location = request.data['location']
        affiliation = request.data['affiliation']

        if (fetched := Personel.objects.filter(title__exact = associate)).exists():
            associate = fetched.get()
        else:
            new_personel = Personel(
                title = associate,
                created_at = timezone.now(),
                content = "",
                private = 1,
                affiliation = None,
                prefix = None,
                connected_account = None
            )
            new_personel.save()
            associate = new_personel
        
        if (fetched := Location.objects.filter(title__exact = location)).exists():
            location = fetched.get()
        else:
            new_location = Location(
                title = location,
                created_at = timezone.now(),
                content = "",
                private = 1
            )
            new_location.save()
            location = new_location
        
        if (fetched := Location.objects.filter(title__exact = affiliation)).exists():
            affiliation = fetched.get()
        else:
            new_location = Location(
                title = location,
                created_at = timezone.now(),
                content = "",
                private = 1
            )
            new_location.save()
            affiliation = new_location

        new_image_case = ImageCase(
            title = title,
            created_at = timezone.now(),
            content = content,
            private = private,
            produced = produced,
            affiliation = affiliation,
            location = location,
            associate = associate
        )
        new_image_case.save()

        
        for person in attendee_list:
            if (fetched := Personel.objects.filter(title__exact = person)).exists():
                new_image_case.attendee.add(fetched.get())
            else:
                new_personel = Personel(
                    title = person,
                    created_at = timezone.now(),
                    content = "",
                    private = 1,
                    affiliation = None,
                    prefix = None,
                    connected_account = None
                )
                new_personel.save()
                new_image_case.attendee.add(new_personel)
    
        


        if (last_index := int(request.data['file_index'])) != -1:
            for i in range(last_index + 1):
                file = request.data[f'{i}']
                file_name = file.name
                file_obj = file
                file_extension = file.name.split('.')[-1]

                new_image_media = ImageMedia(
                        created_at = timezone.now(),
                        name = file_name,
                        extension = file_extension,
                        url = file,
                        )
                new_image_media.save()
                new_image_media.referenced_in.add(new_image_case)
                new_image_media.save()

        new_image_case.save()


        return Response({'message': "file recieved successfully "})


    return Response({'message': ""})


@api_view(['GET', 'POST'])
def video_case_create_view(request):

    def do_after():
        pass

    if request.method == 'POST':
        title = request.data['title']
        content = request.data['content']
        private = request.data['private']
        produced = request.data['produced']
        file_format = request.data['type']
        
        # In case we relate Location, Personel, User to this obj
        # followings are the foreignKey items of ImageCase

        attendee_list = request.data['attendee'].split(',')
        associate = request.data['associate']
        location = request.data['location']
        affiliation = request.data['affiliation']

        if (fetched := Personel.objects.filter(title__exact = associate)).exists():
            associate = fetched.get()
        else:
            new_personel = Personel(
                title = associate,
                created_at = timezone.now(),
                content = "",
                private = 1,
                affiliation = None,
                prefix = None,
                connected_account = None
            )
            new_personel.save()
            associate = new_personel
        
        if (fetched := Location.objects.filter(title__exact = location)).exists():
            location = fetched.get()
        else:
            new_location = Location(
                title = location,
                created_at = timezone.now(),
                content = "",
                private = 1
            )
            new_location.save()
            location = new_location
        
        if (fetched := Location.objects.filter(title__exact = affiliation)).exists():
            affiliation = fetched.get()
        else:
            new_location = Location(
                title = location,
                created_at = timezone.now(),
                content = "",
                private = 1
            )
            new_location.save()
            affiliation = new_location

        new_video_case = VideoCase(
            title = title,
            created_at = timezone.now(),
            content = content,
            private = private,
            produced = produced,
            affiliation = affiliation,
            location = location,
            associate = associate
        )
        new_video_case.save()

        
        for person in attendee_list:
            if (fetched := Personel.objects.filter(title__exact = person)).exists():
                new_video_case.attendee.add(fetched.get())
            else:
                new_personel = Personel(
                    title = person,
                    created_at = timezone.now(),
                    content = "",
                    private = 1,
                    affiliation = None,
                    prefix = None,
                    connected_account = None
                )
                new_personel.save()
                new_video_case.attendee.add(new_personel)
                
    


        if (last_index := int(request.data['file_index'])) != -1:
            for i in range(last_index + 1):
                file = request.data[f'{i}']
                file_name, file_extension = os.path.splitext(file.name)
                file_obj = file
                date = timezone.now().date().__str__().replace('-', '')

                new_video_media = VideoMedia(
                        created_at = timezone.now(),
                        name = file_name,
                        extension = file_extension,
                        archive = file,
                        )

                new_video_media.save()
                new_video_media.referenced_in.add(new_video_case)

                file_name = new_video_media.name
                
                video_url = os.path.join(settings.MEDIA_ROOT, new_video_media.archive.__str__())
                new_url = os.path.join(settings.ARCHIVE_ROOT, f'{date}/video/{file_name}.mp4')
                thumbnail_url = os.path.join(settings.ARCHIVE_ROOT, f'{date}/thumbnail/{file_name}.jpg')

                try:
                    status = settings.PROCESS_STATUS[file_name] = {'encoding': True,
                                                                   'started_at': timezone.now(),
                                                                   'ended_at': None}
                    
                    print(f"{file_name}'s encoding process started at {status['started_at']}%")

                    encoding_processor = subprocess.Popen(
                        f"python3 ./sample_backend/VideoProcessors/videoconverter.py '{video_url}' '{new_url}' '{file_name}'",
                        text = True,
                        shell = True,
                        stdout = subprocess.PIPE,
                        universal_newlines=True)

                    try:
                        outs, errors = encoding_processor.communicate()
                        settings.PROCESS_STATUS[file_name] = {'encoding': False,
                              'started_at': status['started_at'],
                              'ended_at': timezone.now()}
                        print(f"{file_name}'s encoding process ended at {settings.PROCESS_STATUS[file_name]['ended_at']}%")
                    except:
                        encoding_processor.kill()

                    thumbnail_processor = subprocess.Popen(
                        f"python3 ./sample_backend/VideoProcessors/thumbnail_generator.py '{new_url}' '{thumbnail_url}'",
                        text = True,
                        shell = True,
                        stdout = subprocess.PIPE,
                        universal_newlines=True
                    )

                    try:
                        outs, errors = thumbnail_processor.communicate()
                        new_video_media.url = f'/archive/{date}/video/{file_name}.mp4'
                        new_video_media.thumbnail = f'/archive/{date}/thumbnail/{file_name}.jpg'
                        new_video_media.save()
                        print(f'thumbnail generated at {thumbnail_url}')


                    except:
                        thumbnail_processor.kill()

                except:
                    print("Error occurred in codec conversion")
                    if os.path.exists(new_url):
                        os.remove(new_url)
                        print(f"{new_url} file removed successfully")
                    new_video_media.delete()

        new_video_case.save()

        return Response({'message': 'Files has been recieved'})


    return Response({'message': ""})

@api_view(['GET'])
def browse_process(request):
    if request.method == "GET":
        print(settings.PROCESS_STATUS)
        return Response({'message': 'process status in terminal', 'status': settings.PROCESS_STATUS.__repr__()})
    return Response({'message': 'wrong method'})



@api_view(['POST'])
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
