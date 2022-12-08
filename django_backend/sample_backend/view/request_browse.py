from json import JSONEncoder
import json
from rest_framework.response import Response
from rest_framework import exceptions, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.pagination import PageNumberPagination
from drf_multiple_model.pagination import MultipleModelLimitOffsetPagination
from drf_multiple_model.views import FlatMultipleModelAPIView


from converter import Converter
from django.conf import settings

from sample_backend.models import *
from sample_backend.serializer import *
from .utilities import get_user_from_token
from django.utils import timezone


class BrowseRequestAPIView(FlatMultipleModelAPIView):
    # Request view does not support pagination
    permission_classes = [IsAdminUser]
    add_model_type = True
    sorting_fields = ['-created_at']

    def get_querylist(self):

        authority_request_to_join = AuthorityRequest.objects.filter(status__exact = 2)
        access_request_to_join = AccessRequest.objects.filter(status__exact = 2)

        # un_sorted_queryset = activity_serializer.data + team_serializer.data + team_player_left_serializer.data

        querylist = (
            {'queryset': authority_request_to_join.distinct(), 'serializer_class': AuthorityRequestSerializer},
            {'queryset': access_request_to_join.distinct(), 'serializer_class': AccessRequestSerializer},
        )

        return querylist

def single_request(request, request_id, request_form):
    if request.method == "GET":
        if request_form == 0:
            request_model = AccessRequest
            request_serializer = AccessRequestSerializer
        elif request_form == 1:
            request_model = AuthorityRequest
            request_serializer = AuthorityRequestSerializer
        try:
            request_obj = request_model.objects.get(id = request_id)
            serialized_request = request_serializer(request_obj).data
            return Response(serialized_request, status = status.HTTP_200_OK)
        except:
            return Response({"message": "Request object with given id doesn't exists"},
                status = status.HTTP_404_NOT_FOUND)
    return Response({"message": "wrong method call"},
        status = status.HTTP_405_METHOD_NOT_ALLOWED)
