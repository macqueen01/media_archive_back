from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import exceptions
from drf_multiple_model.pagination import MultipleModelLimitOffsetPagination
from drf_multiple_model.views import FlatMultipleModelAPIView

from django.conf import settings

from .models import *
from .serializer import *
from .view import case_browse, case_upload, utilities, user_control


class UserListAPI(APIView):
    def get(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many = True)
        return Response(serializer.data)


@api_view(['POST'])
def image_case_create_view(request):
    return case_upload.image(request)

@api_view(['POST'])
def video_case_create_view(request):
    return case_upload.video(request)

@api_view(['POST'])
def codec_check(request):
    return utilities.codec_check(request)

@api_view(['GET'])
def case_browse_view(request, form):
    return case_browse.main(request, form)

@api_view(['GET'])
def case_browse_detail(request, form, id):
    return case_browse.detail(request, form, id)

@api_view(['GET'])
def browse_process(request):
    if request.method == "GET":
        print(settings.PROCESS_STATUS)
        return Response({'message': 'process status in terminal', 'status': settings.PROCESS_STATUS.__repr__()})
    return Response({'message': 'wrong method'})

@api_view(['POST'])
def create_user(request):
    return user_control.create_user(request)

@api_view(['POST'])
def login_user(request):
    return user_control.login_user(request)

class ResponseThen(Response):
    def __init__(self, data, then_callback, **kwargs):
        super().__init__(data, **kwargs)
        self.then_callback = then_callback

    def close(self):
        super().close()
        self.then_callback()

"""

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
"""



