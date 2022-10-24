from django.shortcuts import render
import asyncio
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from .models import User, Location, Personel, DocCase, ImageCase, VideoCase
from .serializer import UserSerializer, ImageCaseUploadSerializer
from rest_framework import exceptions

# Create your views here.

class UserListAPI(APIView):
    def get(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many = True)
        return Response(serializer.data)

class CaseFromIdAPI(APIView):
    def get(self, request, case_id):
        queryset = ImageCase.objects.filter(id = case_id)
        if queryset.exists():
            serializer = ImageCaseUploadSerializer(queryset, many = True)
            return Response(serializer.data)
        else:
            raise exeptions.NotFound(f"Case id {case_id} not found")

        """
        if addes .value() to filter() then SRC returns null
        """
        
        serializer = ImageCaseUploadSerializer(queryset, many = True)
        return Response(serializer.data)


class CaseListAPI(APIView):
    def get(self, request):
        queryset = ImageCase.objects.all()
        serializer = ImageCaseUploadSerializer(queryset, many = True)
        return Response(serializer.data)

class ImageCaseCreateAPI(CreateAPIView):
    serializer_class = ImageCaseUploadSerializer

    def post(self, request, *args, **kwargs):
        # Here we create Media Object and then pass the object's pk to get_serializer
        if request.FILES:
            media_list = create_image_media(request.FILES)
            return self.create(request, *args, **kwargs)
        return self.create(request, *args, **kwargs)

    async def create_image_media(files):
        