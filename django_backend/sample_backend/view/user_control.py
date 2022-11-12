from json import JSONEncoder
import json
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions, status
from rest_framework.pagination import PageNumberPagination
from drf_multiple_model.pagination import MultipleModelLimitOffsetPagination
from drf_multiple_model.views import FlatMultipleModelAPIView
from knox.models import AuthToken 

from converter import Converter
from django.conf import settings

from sample_backend.models import *
from sample_backend.serializer import *
from django.utils import timezone

def create_user(request):
    if request.method == 'POST':
        if (len(request.data['username']) < 6) or (len(request.data['password']) < 6):
            message = {'message': "short field"}
            return Response(message, status = status.HTTP_400_BAD_REQUEST)
            
        serializer = CreateUserSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.save()

        return Response(
            {
                "user": UserSerializer(user).data,
                "token": AuthToken.objects.create(user)[1]
            }
        )
    return Response({'message': "wrong method call"}, status = status.HTTP_405_METHOD_NOT_ALLOWED)

def login_user(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data
        return Response(
            {
                'user': UserSerializer(user).data,
                'token': AuthToken.objects.create(user)[1]
            }
        )

def process_request(request):
    if request.method == 'POST':
        request_form = request.data['request_form']
        request_id = request.data['request_id']

        if request_form == 0:
            request_obj = AccessRequest.objects.filter(id__exact = request_id)
            return process_access_request(request_obj, request) 
        elif request_form == 1:
            request_obj = AuthorityRequest.objects.filter(id__exact = request_id)
            return process_authority_request(request_obj, request)
        return Response({"message": 'wrong permission request form'}, 
            status = status.HTTP_400_BAD_REQUEST)

def process_access_request(permission_request_set, request):

    if not permission_request_set.exists():
        return Response({'message': "request object with given id not found"}, 
            status = status.HTTP_404_NOT_FOUND)
    

    permission_request_obj = permission_request_set.get()
    request_subject = AccessRequest.objects.get_subject(permission_request_obj)

    
    # IMPORTANT! let permission pair for request.data['image_case'] be {'case_id': "permission_result"}
    for request_component in permission_request_obj.request_components:

        case_form = request_component.requesting_case_form

        if (case_form == 0) and (status := request.data['image_case'][f'{case.id}'] in [0,1,2]):

            case = request_component.image_case
            request_component.status = status
            # message_obj = Message(...)
            
        elif (case_form == 1) and (status := request.data['video_case'][f'{case.id}'] in [0,1,2]):

            case = request_component.video_case
            request_component.status = status
            # message_obj = Message(...)

        elif (case_form == 2) and (status := request.data['doc_case'][f'{case.id}'] in [0,1,2]):

            case = request_component.doc_case
            request_component.status = status
            # message_obj = Message(...)

        else:
            return Response({"message": "access request was sent with invalid status or invalid form in access request detected"},
                status = status.HTTP_400_BAD_REQUEST)

        AccessRequestComponent.grant_permission_to(case, request_subject, request_component.status)
    
    return Response({'message': "user access request resolved"},
        status = status.HTTP_200_OK)
            
        

def process_authority_request(permission_request_set, request):

    if not permission_request_set.exists():
        return Response({"messsage": "request object with given id not found"},
            status = status.HTTP_404_NOT_FOUND)
    
    permission_request_obj = permission_request_set.get()
    request_subject = permission_request_set.get_subject()
    level = permission_request_obj.auth_to


    # when request accepted

    if (request.data['status'] == 1):

        permission_request_obj.status = 1

        # level == 0 -> inactive user
        # level == 1 -> active user
        # level == 2 -> staff

        if (level == 1):

            request_subject.is_active = 1

            # should then construct a message for request_subject's inbox
            # message_obj = Message(...)
        
        elif (level == 2):

            request_subject.is_active = 1
            request_subject.is_staff = 1
        
            # message_obj = Message(...)
        
        else:
            permission_request_obj.status = 0

            # message object sent with rejection status
            # message_obj = Message(...)
            
            return Response({"message": "authority renew request was sent with invalid authority level"},
                status = status.HTTP_501_NOT_IMPLEMENTED)
        

    elif (request.data['status'] == 0):

        permission_request_obj.status = 0
        
        # should make a message object with rejection status (status == 0)
        # message_obj = Message(...)

        return Response({"message": "successfully rejected the request"},
            status = status.HTTP_200_OK)
        
    elif (request.data['status'] == 2):

        permission_request_obj.status = 2

        return Response({"message": "successfully pended the request"},
            status = status.HTTP_200_OK)

    
    return Response({"message": "invalid status detected"},
        status = status.HTTP_400_BAD_REQUEST)






