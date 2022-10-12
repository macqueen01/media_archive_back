from django.urls import path, include
from .views import UserListAPI, CaseListAPI, CaseFromIdAPI

urlpatterns = [
    path('', UserListAPI.as_view()),
    path('cases/', CaseListAPI.as_view()),
    path('cases/<int:case_id>', CaseFromIdAPI.as_view())
]
