from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Case
from .serializer import UserSerializer, CaseUploadSerializer
from rest_framework import exceptions

# Create your views here.

class UserListAPI(APIView):
    def get(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many = True)
        return Response(serializer.data)

class CaseFromIdAPI(APIView):
    def get(self, request, case_id):
        queryset = Case.objects.filter(id = case_id)
        if queryset.exists():
            serializer = CaseUploadSerializer(queryset, many = True)
            return Response(serializer.data)
        else:
            raise exeptions.NotFound(f"Case id {case_id} not found")

        """
        if addes .value() to filter() then SRC returns null
        """
        
        serializer = CaseUploadSerializer(queryset, many = True)
        return Response(serializer.data)


class CaseListAPI(APIView):
    def get(self, request):
        queryset = Case.objects.all()
        serializer = CaseUploadSerializer(queryset, many = True)
        return Response(serializer.data)
    def post(self, request):
        pass