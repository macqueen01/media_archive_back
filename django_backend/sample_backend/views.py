from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework import status
from drf_multiple_model.pagination import MultipleModelLimitOffsetPagination
from drf_multiple_model.views import FlatMultipleModelAPIView

from django.conf import settings

from .models import *
from .serializer import *
from .view import case_browse, case_upload, utilities, \
                  user_control, user_browse, request_processing, \
                  open_request, request_browse, statistics


class UserListAPI(APIView):
    def get(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many = True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def case_count(request):
    return statistics.count_cases(request)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def image_case_create_view(request):
    return case_upload.image(request)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def video_case_create_view(request):
    return case_upload.video(request)

@api_view(['POST'])
def codec_check(request):
    return utilities.codec_check(request)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def case_browse_view(request, form):
    return case_browse.main(request, form)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def case_title_view(request):
    id = int(request.query_params['id'])
    form = int(request.query_params['form'])
    return case_browse.get_case_title(request, form, id)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def case_detail_view(request):
    id = int(request.query_params['id'])
    form = int(request.query_params['form'])
    return case_browse.detail(request, form, id)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def browse_process(request):
    # browses conversion process
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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    return user_control.logout_user(request)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def browse_single_user(request):
    return user_browse.single_user(request)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_status(request):
    return user_browse.single_user(request)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def browse_single_request(request):
    request_id = int(request.query_params['id'])
    request_form = int(request.query_params['form'])
    return request_browse.single_request(request, request_id, request_form)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def search_users(request):
    if search_params := request.query_params['keyword']:
        return user_browse.search_user(request)
    return user_browse.every_user(request)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def resolve_user_request(request):
    # This should return new request array user can browse
    return request_processing.process_request(request)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def open_user_request(request):
    return open_request.open_request(request)




class ResponseThen(Response):
    def __init__(self, data, then_callback, **kwargs):
        super().__init__(data, **kwargs)
        self.then_callback = then_callback

    def close(self):
        super().close()
        self.then_callback()




