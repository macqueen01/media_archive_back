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



def image(request):
    

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

        if (Personel.objects.filter(title__exact = associate)).exists():
            associate = Personel.objects.filter(title__exact = associate).get()
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
        
        if (Location.objects.filter(title__exact = location)).exists():
            location = Location.objects.filter(title__exact = location).get()
        else:
            new_location = Location(
                title = location,
                created_at = timezone.now(),
                content = "",
                private = 1
            )
            new_location.save()
            location = new_location
        
        if (Location.objects.filter(title__exact = affiliation)).exists():
            affiliation = Location.objects.filter(title__exact = affiliation).get()
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
            if (Personel.objects.filter(title__exact = person)).exists():
                new_image_case.attendee.add(Personel.objects.filter(title__exact = person).get())
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
    
        


        if (int(request.data['file_index'])) != -1:
            for i in range(int(request.data['file_index']) + 1):
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



def video(request):

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

        if (Personel.objects.filter(title__exact = associate)).exists():
            associate = Personel.objects.filter(title__exact = associate).get()
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
        
        if (Location.objects.filter(title__exact = location)).exists():
            location = Location.objects.filter(title__exact = location).get()
        else:
            new_location = Location(
                title = location,
                created_at = timezone.now(),
                content = "",
                private = 1
            )
            new_location.save()
            location = new_location
        
        if (Location.objects.filter(title__exact = affiliation)).exists():
            affiliation = Location.objects.filter(title__exact = affiliation).get()
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
            if (Personel.objects.filter(title__exact = person)).exists():
                new_video_case.attendee.add(Personel.objects.filter(title__exact = person).get())
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
                
    


        if (int(request.data['file_index'])) != -1:
            for i in range(int(request.data['file_index']) + 1):
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

        return Response({'message': 'Files has been recieved'},
            status = status.HTTP_200_OK)


    return Response({'message': ""})