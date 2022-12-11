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




def process_request(request):
    if request.method == 'POST':
        request_form = request.data['request_form']
        request_id = request.data['request_id']
        _, token = request.META.get('HTTP_AUTHORIZATION').split(' ')
        processor = get_user_from_token(token)

        if request_form == 0:
            request_obj = AccessRequest.objects.filter(id__exact = request_id)
            return process_access_request(processor, request_obj, request)
        elif request_form == 1:
            request_obj = AuthorityRequest.objects.filter(id__exact = request_id)
            return process_authority_request(processor, request_obj, request)
        return Response({"message": 'wrong permission request form'}, 
            status = status.HTTP_400_BAD_REQUEST)

def process_access_request(processor, permission_request_set, request):

    if not permission_request_set.exists():
        return Response({'message': "request object with given id not found"}, 
            status = status.HTTP_404_NOT_FOUND)
    

    permission_request_obj = permission_request_set.get()
    request_subject = AccessRequest.objects.get_subject(permission_request_obj)

    def content_by_status(user, case, status):
        if status == 0:
            return f"{user.name}님의 '{case.title}' 기록물 접근에 대한 요청이 거절되었습니다"
        elif status == 1:
            return f"{user.name}님의 '{case.title}' 기록물 접근에 대한 요청이 승인되었습니다"
        else:
            return f"{user.name}님의 '{case.title}' 기록물 접근에 대한 요청이 보류되었습니다"


    
    # IMPORTANT! let permission pair for request.data['image_case'] be {'case_id': "permission_result (status)"}
    for request_component in permission_request_obj.request_components.all():

        case_form = request_component.requesting_case_form

        if (case_form == 0):

            case = request_component.image_case
            case_manager = ImageCase.objects
            request_component.status = int(request.data['image_case'][f'{case.id}'])
            request_component.save()

            Message.objects.send(
                sender = processor,
                receiver_set = request_subject,
                content = content_by_status(request_subject, case, request_component.status)
            )

            
        elif (case_form == 1):

            case = request_component.video_case
            case_manager = VideoCase.objects
            request_component.status = int(request.data['video_case'][f'{case.id}'])
            request_component.save()

            Message.objects.send(
                sender = processor,
                receiver_set = request_subject,
                content = content_by_status(request_subject, case, request_component.status)
            )

        elif (case_form == 2):

            case = request_component.doc_case
            case_manager = DocCase.objects
            request_component.status = int(request.data['doc_case'][f'{case.id}'])
            request_component.save()

            Message.objects.send(
                sender = processor,
                receiver_set = request_subject,
                content = content_by_status(request_subject, case, request_component.status)
            )

        else:
            return Response({"message": "access request was sent with invalid status or invalid form in access request detected"},
                status = status.HTTP_400_BAD_REQUEST)
        
        # permission object status always set "accpeted" so that
        # when displayed in request view, the processed permission request is not shown

        case_manager.grant_permission_to(case, request_subject, request_component.status)
        
    permission_request_obj.status = 1
    permission_request_obj.save()
    
    return Response({'message': "user access request resolved"},
        status = status.HTTP_200_OK)
            
        

def process_authority_request(processor, permission_request_set, request):

    if not permission_request_set.exists():
        return Response({"messsage": "request object with given id not found"},
            status = status.HTTP_404_NOT_FOUND)
    
    permission_request_obj = permission_request_set.get()
    request_subject = AuthorityRequest.objects.get_subject(permission_request_obj)
    level = permission_request_obj.auth_to


    # when request accepted

    if (int(request.data['status']) == 1):

        permission_request_obj.status = 1

        # level == 0 -> inactive user
        # level == 1 -> active user
        # level == 2 -> staff

        if (level == 1):

            request_subject.is_active = 1

            # should then construct a message for request_subject's inbox
            Message.objects.send(
                sender = processor,
                receiver_set = request_subject,
                content =f"{request_subject.name}님의 계정이 활성화 되었습니다"
                )
        
        elif (level == 2):

            request_subject.is_active = 1
            request_subject.is_staff = 1
        
            Message.objects.send(
                sender = processor,
                receiver_set = request_subject,
                content =f"{request_subject.name}님의 계정이 관리자로 승격 되었습니다"
                )
        
        else:
            permission_request_obj.status = 0
            permission_request_obj.save()

            # message object sent with rejection status
            Message.objects.send(
                sender = processor,
                receiver_set = request_subject,
                content =f"{request_subject.name}님의 요정에 문제가 있습니다"
                )
            
            return Response({"message": "authority renew request was sent with invalid authority level"},
                status = status.HTTP_501_NOT_IMPLEMENTED)
        
        permission_request_obj.save()
        request_subject.save()

        return Response({"message": "Authority renew has been successful"},
            status = status.HTTP_200_OK)

    elif (int(request.data['status']) == 0):

        permission_request_obj.status = 0
        permission_request_obj.save()
        
        # should make a message object with rejection status (status == 0)
        Message.objects.send(
                sender = processor,
                receiver_set = request_subject,
                content =f"{request_subject.name}님의 권한변경 요정이 거절되었습니다"
                )

        return Response({"message": "successfully rejected the request"},
            status = status.HTTP_200_OK)
        
    elif (int(request.data['status']) == 2):

        permission_request_obj.status = 2
        permission_request_obj.save()

        return Response({"message": "successfully pended the request"},
            status = status.HTTP_200_OK)

    
    return Response({"message": "invalid status detected"},
        status = status.HTTP_400_BAD_REQUEST)






