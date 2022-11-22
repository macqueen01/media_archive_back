from django.urls import path, include
from .views import *

urlpatterns = [
    path('', UserListAPI.as_view()),
    path('cases/create/0', image_case_create_view),
    path('cases/create/1', video_case_create_view),
    path('cases/browse/<int:form>', case_browse_view),
    path('cases/browse/detail', case_detail_view),
    path('cases/browse/status', browse_process),
    path('cases/codec', codec_check),
    path('user/create', create_user),
    path('user/login', login_user),
    path('user/check-status', check_status),
    path('request/resolve', resolve_user_request),
    path('request/open', open_user_request),
    path('request/browse', request_browse.BrowseRequestAPIView.as_view())
    #path('cases/browse/<int:id>', browse_detail_view)
]
