from django.urls import path, include
from .views import *

urlpatterns = [
    path('', UserListAPI.as_view()),
    path('cases/create/0', image_case_create_view),
    path('cases/create/1', video_case_create_view),
    path('cases/browse/<int:form>', case_browse_view),
    path('cases/browse/status', browse_process),
    path('cases/codec', codec_check),
    path('cases/browse/<int:form>/<int:id>', case_browse_detail),
    path('user/create', create_user),
    path('user/login', login_user),
    path('user/check-status', check_status)
    #path('cases/browse/<int:id>', browse_detail_view)
]
