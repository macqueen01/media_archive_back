from django.urls import path, include
from .views import *

urlpatterns = [
    path('', UserListAPI.as_view()),
    path('cases/create/0', image_case_create_view),
    path('cases/create/1', video_case_create_view)
]
