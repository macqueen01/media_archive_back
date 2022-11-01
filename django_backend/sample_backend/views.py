from json import JSONEncoder
import json
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.pagination import PageNumberPagination


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

@api_view(['GET'])
def browse_view(request):
    if request.method == 'GET':
        cases = ImageCase.objects.all()

        paginator = PageNumberPagination()
        paginator.page_size = 1
        browse_cases = ImageCase.objects.all()
        result_page = paginator.paginate_queryset(browse_cases, request)
        serializer = BrowseCaseSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    return Response({'message': "wrong method call"})

@api_view(['GET'])
def browse_detail(request, int):
    key = int
    if request.method == 'GET':
        try:
            form = int(request.GET['_type'])
            if (form == 0):
                browse_object = ImageCase.objects.filter(id__exact = key)
            elif (form == 1):
                browse_object = VideoCase.objects.filter(id__exact = key)
            elif (form == 2):
                browse_object = DocCase.objects.filter(id__exact = key)
            else:
                return Response({'message': 'The file type requested cannot be browsed'})
            
            if (not browse_object.exists()):
                return Response({'message': 'The file with given id does not exist'})
            else:
                pass

        except:
            return Response({'message': 'The file type has not submitted'})

@api_view(['GET','POST'])
def image_case_create_view(request):

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


        return Response({'message': 'Files has been recieved'})


    return Response({'message': ""})


@api_view(['GET', 'POST'])
def video_case_create_view(request):

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
                file_name = file.name
                file_obj = file
                file_extension = file.name.split('.')[-1]

                new_video_media = VideoMedia(
                        created_at = timezone.now(),
                        name = file_name,
                        extension = file_extension,
                        url = file,
                        )

                new_video_media.save()
                new_video_media.referenced_in.add(new_video_case)
                
                video_url = os.path.join(settings.MEDIA_ROOT, new_video_media.url.__str__())
                new_url = os.path.join(settings.MEDIA_ROOT, f'./archive/{file_name}.mp4')

                try:
                    status = settings.PROCESS_STATUS[file_name] = {'encoding': True,
                                                                   'started_at': timezone.now(),
                                                                   'ended_at': None}
                    
                    print(f"{file_name}'s encoding process started at {status['started_at']}%")

                    sub = subprocess.Popen(
                        f"python3 ./sample_backend/VideoProcessors/videoconverter.py '{video_url}' './media/archive/{file_name}.mp4' '{file_name}'",
                        text = True,
                        shell = True,
                        stdout = subprocess.PIPE,
                        universal_newlines=True)

                    
                    settings.PROCESS_STATUS[file_name] = {'encoding': False,
                              'started_at': status['started_at'],
                              'ended_at': timezone.now()}
                        
                    print(f"{file_name}'s encoding process ended at {settings.PROCESS_STATUS[file_name]['ended_at']}%")

                except:
                    print("Error occurred in codec conversion")
                
                new_video_media.url = f'/archive/{file_name}.mp4'
                new_video_media.save()

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
                        url = file,
                        )
                new_video_media.save()

                video_url = os.path.join(settings.MEDIA_ROOT, new_video_media.url.__str__())
                
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
