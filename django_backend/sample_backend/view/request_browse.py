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
