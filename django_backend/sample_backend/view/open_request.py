from json import JSONEncoder
from rest_framework.response import Response
from rest_framework import status

from knox.models import AuthToken
from knox.settings import CONSTANTS

from converter import Converter
from django.conf import settings

from sample_backend.models import *
from sample_backend.serializer import *
from django.utils import timezone
from knox.settings import CONSTANTS
from .utilities import get_user_from_token, case_id_map_parser



def open_request(request):
    if request.method == "POST":
        request_form = request.data['request_form']
        _, token = request.META.get('HTTP_AUTHORIZATION').split(' ')
        user = get_user_from_token(token)

        if request_form == 1:
            return open_authority_request(user, request)
        elif request_form == 0:
            return open_access_request(user, request)
        
        return Response({"message": "wrong request form sent. aborted."},
            status = status.HTTP_400_BAD_REQUEST)
    return Response({"message": "wrong method call on open_request"},
        status = status.HTTP_405_METHOD_NOT_ALLOWED)

def open_authority_request(user, request):
    if result := AuthorityRequest.objects.open_request(
        user = user,
        title = request.data['title'],
        comments = request.data['comments'],
        auth_from = request.data['auth_from'],
        auth_to = request.data['auth_to']
    ):
        return Response({'message': "opened authority request successfully"},
            status = status.HTTP_200_OK)
    return Response({'message': "authority change request ran into a problem"},
        status = status.HTTP_409_CONFLICT)


def open_access_request(user, request):
    case_id_map = case_id_map_parser(request)
    AccessRequest.objects.open_request(
        user = user,
        title = request.data['title'],
        comments = request.data['comments'],
        case_id_map = case_id_map
    )

    return Response({"message": "opened access request successfully"})


