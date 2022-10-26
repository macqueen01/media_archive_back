from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from .models import *
from .serializer import *
from rest_framework import exceptions
from django.utils import timezone

# Create your views here.

class UserListAPI(APIView):
    def get(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many = True)
        return Response(serializer.data)


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
                new_video_media.save()

        new_video_case.save()

        return Response({'message': 'Files has been recieved'})


    return Response({'message': ""})
